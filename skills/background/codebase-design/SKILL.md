---
name: codebase-design
description: Deep-module design vocabulary and principles. Use when designing or improving a module's interface, deciding where a seam goes, deepening shallow modules, or making code more testable or AI-navigable.
license: MIT
---

# Codebase Design

Design **deep modules**: a lot of behavior behind a small interface, placed at a clean seam, testable through that interface.

## Glossary

Use these terms exactly, in place of the words each entry lists under _Avoid_: consistent language is the whole point.

**Module**: anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice. _Avoid_: unit, component, service.

**Interface**: everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API, signature, the TypeScript `interface` keyword, a class's public methods (all too narrow: they name only the type-level surface).

**Implementation**: what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**: leverage at the interface. The amount of behavior a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behavior sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation. Ousterhout weighs the functionality a module provides against the complexity of its interface; measure that leverage, not a ratio of implementation lines to interface lines, which rewards padding the implementation.

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘

┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

**Seam** _(Michael Feathers)_: a place where you can alter behavior without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it. _Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter**: a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

**Leverage**: what callers get from depth. One implementation pays back across N call sites and M tests.

**Locality**: what maintainers get from depth. Change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts; they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape; a test that must change when only the implementation changes is testing past it.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Introduce a seam only when something actually varies across it, typically a production adapter and a test adapter; a single-adapter seam is just indirection.

## Designing for testability

- **Accept dependencies** instead of constructing them inside the module.
- **Return results** instead of producing side effects.
- **Shrink the surface**: fewer methods, simpler parameters, more complexity hidden inside. Each cut means fewer tests and simpler test setup.

## Going deeper

- When deepening a cluster of shallow modules, read [DEEPENING.md](DEEPENING.md) for dependency categories and replace-don't-layer testing.
- When exploring alternative interfaces for a deepening candidate, read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) for the Design It Twice pattern.
