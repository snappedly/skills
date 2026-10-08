# UI Prototype

Build the smallest visual experiment that answers the question.

## Two sub-shapes: strongly prefer sub-shape A

A UI prototype is much easier to judge when it's **butting up against the rest of the app**: real header, real sidebar, real data, real density. A throwaway route on its own is a vacuum: every variant looks fine in isolation, and the design problems a populated page would expose stay hidden.

### Sub-shape A: adjustment to an existing page (preferred)

The route already exists. Variants are rendered **on the same route**, gated by a `?variant=` URL search param; only the rendering swaps. This is the default whenever there's a plausible existing page to host the variants.

Something that doesn't yet have a page but _would naturally live inside one_ (a new section of the dashboard, a new card on the settings screen, a new step in an existing flow) is still sub-shape A: mount the variants inside the host page.

### Sub-shape B: a new page (last resort)

Only when the thing being prototyped genuinely has no existing page to live inside (an entirely new top-level surface, or a flow that can't be embedded anywhere sensible). Create a **throwaway route** following the routing convention the project already uses, named so it's obviously a prototype (for example, include the word `prototype` in the path or filename), with the same `?variant=` pattern.

## Process

### 1. State the question and pick N

For a requested comparison, default to **3 variants**, at most 5. For one concrete design question or a user-specified treatment, build one useful example and skip the variant switcher below; add alternatives only if comparison would answer the question.

Write down the plan in one line, in the prototype's location or a top-of-file comment:

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

### 2. Generate radically different variants

Use the user's brief as the direction, within the design system, tokens, and visual direction `docs/agents/frontend.md` records when present, else the project's existing components and styles. Clarify only a missing decision that prevents a useful experiment.

Draft each variant. Hold each one to:

- The page's purpose and the data it has access to.
- The project's component library and styling system.
- A clear exported component name, such as `VariantA`, `VariantB`, or `VariantC`.

Variants must be **structurally different** within the brief: different layout, different information hierarchy, different primary affordance, not just different colors or copy. Three slightly-tweaked card grids isn't a UI prototype, it's wallpaper. If two drafts come out too similar, redo one around a structure the others lack.

Each variant owns its layout: share leaf components such as a `<Header>`, never a `<Layout>`, so every variant is free to throw the layout out.

Variants read real data. Point any mutation at a stub: the question is "what should this look like", not "does the backend work".

### 3. Wire them together

Create a single switcher component on the route:

```tsx
// pseudo-code, adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

For sub-shape A (existing page): keep all the existing data fetching, params, and auth above the switcher; only the rendered subtree changes per variant.

For sub-shape B (new page): the throwaway route mounts the same switcher.

### 4. Build the floating switcher

A small fixed-position bar at the bottom-center of the screen with three pieces:

- **Left arrow**: cycles to the previous variant (wraps around).
- **Variant label**: shows the current variant key and, if the variant exports a name, that name too, such as `B (Sidebar layout)`.
- **Right arrow**: cycles forward (wraps around).

Behavior:

- Clicking an arrow updates the URL search param (use the framework's router, such as `router.replace` in Next.js or `navigate` in React Router) so the variant is shareable and reload-stable.
- Keyboard: `←` and `→` also cycle, except while an `<input>`, `<textarea>`, or `[contenteditable]` has focus.
- Visually distinct from the page (such as a high-contrast pill or a subtle shadow) so it's obviously not part of the design being evaluated.
- Hidden in production builds: gate on `process.env.NODE_ENV !== 'production'` or an equivalent check, so a stray prototype merge can't ship the bar to users.

Make the switcher a single shared component, placed wherever the project keeps shared UI, so both sub-shapes can reuse it.

### 5. Hand it over

Surface the URL (and the `?variant=` keys). The interesting feedback is usually **"I want the header from B with the sidebar from C"**, which is the actual design they want.

### 6. Capture the answer and clean up

Once a variant has won, capture the answer (which variant and why) and settle the prototype files as **Capture the answer** in [SKILL.md](SKILL.md) describes. When folding it into production is authorized, rewrite the winner properly as you go, since it was written under prototype constraints, and take the rest out of the base branch, since variant components and a switcher left there rot fast and confuse the next reader:

- **Sub-shape A**: fold the winner into the existing page; drop the losing variants and the switcher.
- **Sub-shape B**: promote the winning variant to a real route; drop the throwaway route and the switcher.
