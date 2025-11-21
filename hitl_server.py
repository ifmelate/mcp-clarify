#!/usr/bin/env python3

"""
Minimal MCP HITL server

Exposes a single tool `ask_clarification` that elicits structured user input
via MCP elicitation (rendered by clients like Cursor, VS Code, Claude Desktop).

Run locally (stdio transport):
  uv venv && uv pip install fastmcp
  python hitl_server.py

Then register this server in your MCP-enabled client configuration
as a stdio server that runs `python hitl_server.py`.

For full documentation, see README.md
"""

from typing import Any, Dict, List, Optional, Literal
from dataclasses import dataclass
try:
    from pydantic import BaseModel  # Prefer Pydantic v2 if available
    import pydantic as _p
    _PYDANTIC_MAJOR = int(getattr(_p, 'VERSION', '2').split('.')[0])
except Exception as e:
    # Fall back to a minimal shim if Pydantic is unavailable; we'll use JSON schema instead
    BaseModel = object  # type: ignore
    _PYDANTIC_MAJOR = 0
import inspect

try:
    from mcp.server.fastmcp import FastMCP, Context
    from mcp.server.session import ServerSession
except Exception as e:  # ImportError or SDK not installed
    raise SystemExit(
        "MCP Python SDK not installed. Install with:\n"
        "  uv venv && uv pip install fastmcp\n"
        f"Import error: {e}"
    )


mcp = FastMCP("mcp-clarify")


class ClarifyAnswer(BaseModel):
    """Pydantic model used to render a simple one-field form in MCP clients."""
    answer: str  # Short answer (<= 5 words)

# Provide a v1-to-v2 compatibility shim if running on Pydantic v1
try:
    if _PYDANTIC_MAJOR and _PYDANTIC_MAJOR < 2:  # pragma: no cover
        # Map v2-style attribute expected by some FastMCP builds
        setattr(ClarifyAnswer, 'model_fields', getattr(ClarifyAnswer, '__fields__', {}))  # type: ignore[attr-defined]
except Exception:
    pass


@mcp.tool()
async def ask_clarification(ctx: Context[ServerSession, None], prompt: str, choices: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Ask a single clarification question and capture a concise answer.

    Uses FastMCP elicitation with response_type (not response_schema) so that
    MCP clients (Cursor, VS Code, Claude Desktop) render a small input form.

    Args:
        prompt: The human-visible question to ask (e.g., "Pick target latency SLA?")
        choices: Optional list of suggested answers. When provided, clients that
            honor JSON Schema enums will render these as selectable options.

    Returns:
        JSON with fields: {"question": str, "answer": str}
    """
    # Be compatible across FastMCP variants by trying multiple signatures.
    # We'll attempt several combinations in order, catching TypeError and moving on.
    # Also handle both "message" and "prompt" as the text key.
    tried_errors = []
    for text_key in ("message", "prompt"):
        # Show choices on separate lines for readability.
        display_prompt = prompt
        if choices:
            lines = "\n".join(f"{i+1}) {str(c)}" for i, c in enumerate(choices))
            display_prompt = f"{prompt}\n\nOptions:\n{lines}\n(Type the value or its number)"
        message_kwargs: Dict[str, Any] = {text_key: display_prompt}
        # 0) JSON Schema dict (most portable across SDK variants)
        answer_schema: Dict[str, Any] = {"type": "string", "title": "Answer"}
        if choices:
            # Provide an enum to let clients render a select/radio UI.
            # Dedupe while preserving order and coerce values to strings.
            answer_schema["enum"] = list(dict.fromkeys([str(c) for c in choices]))
            # Also include oneOf with const+title for clients that surface labels from oneOf
            answer_schema["oneOf"] = [
                {"const": str(c), "title": str(c)} for c in answer_schema["enum"]
            ]

        schema_json: Dict[str, Any] = {
            "type": "object",
            "title": "ClarifyAnswer",
            "properties": {"answer": answer_schema},
            "required": ["answer"],
            "additionalProperties": False,
        }
        try:
            result = await ctx.elicit(**message_kwargs, response_schema=schema_json)  # type: ignore[call-arg]
            break
        except Exception as e:
            tried_errors.append(str(e))
        try:
            result = await ctx.elicit(**message_kwargs, schema=schema_json)  # type: ignore[call-arg]
            break
        except Exception as e:
            tried_errors.append(str(e))
        try:
            result = await ctx.elicit(schema_json, **message_kwargs)  # type: ignore[misc]
            break
        except Exception as e:
            tried_errors.append(str(e))
        # 0b) If schemas are ignored but response_type is honored, construct
        #     a dynamic Pydantic model with Literal[...] to encode choices.
        dynamic_model = None
        if choices:
            try:
                from pydantic import create_model  # type: ignore
                allowed = tuple(str(c) for c in list(dict.fromkeys(choices)))
                # Create Literal at runtime
                AnswerLiteral = Literal[allowed]  # type: ignore[misc]
                dynamic_model = create_model("ClarifyAnswerChoices", answer=(AnswerLiteral, ...))  # type: ignore[assignment]
            except Exception as e:
                tried_errors.append(str(e))
        if dynamic_model is not None:
            try:
                result = await ctx.elicit(**message_kwargs, response_type=dynamic_model)  # type: ignore[call-arg]
                break
            except Exception as e:
                tried_errors.append(str(e))
        try:
            result = await ctx.elicit(**message_kwargs, response_type=ClarifyAnswer)  # type: ignore[call-arg]
            break
        except Exception as e:
            tried_errors.append(str(e))
        try:
            result = await ctx.elicit(**message_kwargs, response_schema=ClarifyAnswer)  # type: ignore[call-arg]
            break
        except Exception as e:
            tried_errors.append(str(e))
        try:
            result = await ctx.elicit(**message_kwargs, response_model=ClarifyAnswer)  # type: ignore[call-arg]
            break
        except Exception as e:
            tried_errors.append(str(e))
        try:
            result = await ctx.elicit(**message_kwargs, schema=ClarifyAnswer)  # type: ignore[call-arg]
            break
        except Exception as e:
            tried_errors.append(str(e))
        try:
            # Some versions require positional schema first
            result = await ctx.elicit(ClarifyAnswer, **message_kwargs)  # type: ignore[misc]
            break
        except Exception as e:
            tried_errors.append(str(e))
        try:
            # As a last resort, try without schema and coerce later
            result = await ctx.elicit(**message_kwargs)  # type: ignore[call-arg]
            break
        except Exception as e:
            tried_errors.append(str(e))
    else:
        # If we exhausted loops without break, raise a helpful error
        raise TypeError("ctx.elicit signature not compatible; tried variants: " + " | ".join(tried_errors))

    answer = ""
    # FastMCP returns an object with fields like action (accept/decline/cancel) and data
    action = getattr(result, "action", None)
    data = getattr(result, "data", None)
    if action == "accept" and data is not None:
        try:
            # Handle dataclass-like, dict, or simple types
            if hasattr(data, "answer"):
                answer = str(getattr(data, "answer")).strip()
            elif isinstance(data, dict):
                answer = str(data.get("answer", "")).strip() or str(data).strip()
            else:
                answer = str(data).strip()
        except Exception:
            answer = str(data).strip()
    else:
        # If no action/data contract, attempt direct extraction
        try:
            if hasattr(result, "answer"):
                answer = str(getattr(result, "answer")).strip()
            elif isinstance(result, dict) and "answer" in result:
                answer = str(result["answer"]).strip()
            else:
                # Treat entire result as the answer text
                answer = str(result).strip()
        except Exception:
            answer = ""

    # If choices were provided, coerce numeric selection or case-insensitive match
    if choices and isinstance(answer, str):
        raw = answer.strip()
        selected = None
        # Accept formats like "1", "1)", "1.", "1: dev"
        try:
            token = raw.split()[0].rstrip(").:]")
            if token.isdigit():
                idx = int(token)
                if 1 <= idx <= len(choices):
                    selected = str(choices[idx - 1])
        except Exception:
            pass
        if selected is None:
            for c in choices:
                if raw.lower() == str(c).lower():
                    selected = str(c)
                    break
        # Only override when we identified a valid selection
        if selected is not None:
            answer = selected

    return {"question": prompt, "answer": answer}


if __name__ == "__main__":
    mcp.run(transport="stdio")


