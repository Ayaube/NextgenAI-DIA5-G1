#!/usr/bin/env python3
"""TD 2 and TD 3: read the decisions of a routing rule, then adapt it to your own.

Synthetic resources, no API call, no key.

Costs are fictional USD excluding tax per request, with a fixed token envelope.
Capability levels 1/2/3 describe eligibility for this exercise, not model IQ.
Quota availability is supplied as a scenario, not measured from a provider.
"""
import argparse
import json
from urllib import request

# Simulation assumption: 1,500 input tokens and 100 output tokens per call.
# OpenRouter price for GPT-OSS 120B: $0.15 input and $0.60 output per million.
paid_cost = (1_500 * 0.15 + 100 * 0.60) / 1_000_000

RESOURCES = [
    {"id": "groq:openai/gpt-oss-120b", "model": "gpt-oss-120b",
     "access": "free", "cash": 0.0},
    {"id": "groq:openai/gpt-oss-20b", "model": "gpt-oss-20b",
     "access": "free", "cash": 0.0},
    {"id": "groq:qwen/qwen3.8-27b", "model": "qwen3.8-27b",
     "access": "free", "cash": 0.0},
    {"id": "openrouter:cohere/north-mini-code:free", "model": "north-mini-code",
     "access": "free", "cash": 0.0},
    {"id": "openrouter:dots-studio/dots-3-note-preview:free", "model": "dots-3-note",
     "access": "free", "cash": 0.0},
    {"id": "openrouter:openai/gpt-oss-120b", "model": "gpt-oss-120b",
     "access": "tokens", "cash": paid_cost},
]


FAMILY_RULES = {
    "F1": {
        "cells": ["C01", "C04", "C05", "C06", "C07", "C20"],
        "first_model": "gpt-oss-20b",
        "customer_panel": ["gpt-oss-20b", "north-mini-code", "dots-3-note"],
    },
    "F2": {
        "cells": ["C02", "C08", "C09", "C11"],
        "first_model": "gpt-oss-120b",
        "customer_panel": ["gpt-oss-120b", "qwen3.8-27b", "dots-3-note"],
    },
    "F2b": {
        "cells": ["C10"],
        "first_model": "gpt-oss-120b",
        "customer_panel": ["gpt-oss-120b", "qwen3.8-27b", "dots-3-note"],
    },
    "F3": {
        "cells": ["C03", "C12", "C13", "C14"],
        "first_model": "gpt-oss-20b",
        "customer_panel": ["gpt-oss-120b", "north-mini-code", "qwen3.8-27b"],
    },
    "F4": {
        "cells": ["C15", "C16", "C17", "C18", "C19"],
        "first_model": "gpt-oss-120b",
        "customer_panel": ["gpt-oss-120b", "north-mini-code", "qwen3.8-27b"],
    },
}

# Free fallback models, in priority order, when the first model is unavailable.
FREE_FALLBACKS = {
    "F1": ["north-mini-code", "dots-3-note", "gpt-oss-120b", "qwen3.8-27b"],
    "F2": ["qwen3.8-27b"],
    "F2b": ["qwen3.8-27b"],
    "F3": ["dots-3-note", "north-mini-code", "gpt-oss-120b", "qwen3.8-27b"],
    "F4": ["gpt-oss-20b"],
}

def available_free_panel(family, resources):
    """Return the available free voting routes in the family's panel order."""
    available = {
        route["model"]: route["id"]
        for route in resources
        if route["access"] == "free" and route["available"]
    }

    panel = []
    for model in FAMILY_RULES[family]["customer_panel"]:
        if family == "F4" and model == "gpt-oss-120b" and model not in available:
            model = "gpt-oss-20b"

        if model in available:
            panel.append(available[model])

    return panel

def choose(request, resources):
    family = request["family"]
    rule = FAMILY_RULES.get(family)

    if rule is None:
        return {
            "action": "abstain", "resource": None, "cash": 0,
            "checks": None,
            "reason": f"No TD1 evidence for family {family}.",
        }

    evidence = f"{family}, TD1 cells {', '.join(rule['cells'])}"
    use_case = request["use_case"]

    if use_case == "internal_dashboard":
        checks = "read-only SQL execution and integer amount in cents"
    elif use_case == "customer_figure":
        panel = available_free_panel(family, resources)
        calls_left = max(0, 10 - request.get("free_calls_used", 0))
        panel = panel[:calls_left]
        checks = "display only if two distinct panel members agree to the cent"

        if len(panel) >= 2 and request["deadline_minutes"] > 0:
            return {
                "action": "run",
                "resource": panel,
                "cash": 0,
                "checks": checks,
                "required_votes": 2,
                "panel_size": 3,
                "reason": f"{evidence}: enough free panel members to attempt a 2-of-3 vote.",
            }

        deadline = request["deadline_minutes"]

        # Wait only if a second free panel member could become available in time.
        if request["can_wait"] and calls_left >= 2:
            delays = {}
            for route in resources:
                if route["access"] == "free" and not route["available"]:
                    reset = route["reset_minutes"]
                    delays[route["id"]] = 1 if reset is None else reset

            for delay in sorted(set(delays.values())):
                if not 0 < delay < deadline:
                    continue

                projected = [
                    dict(route, available=True)
                    if route["id"] in delays and 0 < delays[route["id"]] <= delay
                    else route
                    for route in resources
                ]
                if len(available_free_panel(family, projected)) >= 2:
                    return {
                        "action": "defer", "resource": None, "cash": 0,
                        "checks": checks, "required_votes": 2, "panel_size": 3,
                        "wake_in_minutes": delay,
                        "reason": f"{evidence}: recheck quorum availability in {delay} min.",
                    }

        # Paid 120B can fill the GPT-OSS seat if another family can also vote.
        paid_id = "openrouter:openai/gpt-oss-120b"
        paid_route = next((r for r in resources if r["id"] == paid_id), None)
        gpt_seat_open = (
            "gpt-oss-120b" in rule["customer_panel"]
            and not any("gpt-oss" in route_id for route_id in panel)
        )
        if (len(panel) == 1 and gpt_seat_open and paid_route
                and paid_route["available"] and paid_route["cash"] <= request["budget"]
                and deadline > 0):
            return {
                "action": "run", "resource": [*panel, paid_id],
                "cash": paid_route["cash"], "checks": checks,
                "required_votes": 2, "panel_size": 3,
                "reason": f"{evidence}: paid 120B adds a second distinct voting family.",
            }

        return {
            "action": "abstain",
            "resource": None,
            "cash": 0,
            "checks": checks,
            "required_votes": 2,
            "panel_size": 3,
            "reason": f"{evidence}: cannot start a free quorum within the current limits.",
        }
    elif use_case == "payout":
        checks = "require an exact match in cents with an independent SQL reference"
        if family in {"F1", "F2", "F2b"}:
            checks += " and human approval before payout"
    else:
        return {
            "action": "abstain", "resource": None, "cash": 0,
            "checks": "pending implementation",
            "reason": f"{evidence}: this use case still needs its own check.",
        }
    model_order = [rule["first_model"], *FREE_FALLBACKS[family]]
    free_routes = [
        route
        for model in model_order
        for route in resources
        if route["model"] == model and route["access"] == "free"
    ]

    # The caller carries this count across retries of the same request.
    if request.get("free_calls_used", 0) < 10:
        for route in free_routes:
            if route["available"]:
                return {
                    "action": "run", "resource": route["id"], "cash": 0,
                    "checks": checks,
                    "reason": f"{evidence}: first available eligible free route.",
                }

        if request["can_wait"]:
            candidates = []
            for route in free_routes:
                delay = route["reset_minutes"]
                if delay is None:
                    delay = 1  # No announced refill: check again in 60 seconds.
                if 0 < delay < request["deadline_minutes"]:
                    candidates.append((delay, route))

            if candidates:
                delay, route = min(candidates, key=lambda item: item[0])
                return {
                    "action": "defer", "resource": route["id"], "cash": 0,
                    "checks": checks, "wake_in_minutes": delay,
                    "reason": f"{evidence}: recheck availability in {delay} min.",
                }

    paid_routes = [
        route for route in resources
        if route["access"] == "tokens"
        and route["model"] in model_order
        and route["available"]
        and route["cash"] <= request["budget"]
    ]
    if paid_routes and request["deadline_minutes"] > 0:
        route = min(paid_routes, key=lambda item: item["cash"])
        return {
            "action": "run", "resource": route["id"], "cash": route["cash"],
            "checks": checks,
            "reason": f"{evidence}: paid fallback fits the remaining budget.",
        }

    return {
        "action": "abstain", "resource": None, "cash": 0,
        "checks": checks,
        "reason": f"{evidence}: no eligible route within deadline and budget.",
    }

def scenarios():
    base = {
        "family": "F1",
        "use_case": "internal_dashboard",
        "can_wait": True,
        "deadline_minutes": 120,
        "budget": 0.30,
    }

    available = [
        dict(route, available=True, reset_minutes=None)
        for route in RESOURCES
    ]

    blocked_ids = {
        "groq:openai/gpt-oss-120b",
        "groq:openai/gpt-oss-20b",
    }
    free_gpt_oss_blocked = [
        dict(route, available=False, reset_minutes=60)
        if route["id"] in blocked_ids else route.copy()
        for route in available
    ]

    f4 = {**base, "family": "F4"}
    urgent = {**f4, "can_wait": False, "deadline_minutes": 5}

    return [
        ("simple", base, available),
        ("complex", f4, available),
        ("deferrable", f4, free_gpt_oss_blocked),
        ("urgent", urgent, free_gpt_oss_blocked),
        ("budget exhausted", {**urgent, "budget": 0}, free_gpt_oss_blocked),
        ("high impact", {**f4, "use_case": "payout"}, available),
        ("unknown capability", {**base, "family": "unknown"}, available),
    ]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", help="show only the named scenario")
    args = parser.parse_args()
    found = False
    for name, request, resources in scenarios():
        if args.scenario and name != args.scenario:
            continue
        found = True
        print(json.dumps({"scenario": name, "nature": "simulation", "request": request,
                          "result": choose(request, resources)}))
    if not found:
        parser.error("unknown scenario")


if __name__ == "__main__":
    main()
