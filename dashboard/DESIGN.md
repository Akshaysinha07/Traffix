# Design System Specification: Industrial Intelligence

## 1. Overview & Creative North Star
This design system is built to evoke **"The Precision Monolith."** We are moving away from the "hacker" aesthetic of neon-on-black and entering the realm of high-end industrial engineering. The objective is to create a digital environment that feels as heavy and reliable as a steel beam, yet as precise as a Swiss timepiece.

### The Creative North Star: Kinetic Blueprint
The "Kinetic Blueprint" philosophy dictates that every element must feel like it has a structural purpose. We achieve an editorial, high-end look by rejecting the generic "dashboard grid" in favor of intentional asymmetry. Large, authoritative typography headers should anchor pages, while data containers utilize overlapping layers and varied tonal depths to guide the eye. This is not a "sci-fi" interface; it is a sophisticated tool for professionals who value clarity over decoration.

---

## 2. Colors & Tonal Architecture
The palette has evolved into a sophisticated, low-contrast "Tonal Spot" arrangement, moving from vibrant signals to muted, professional steel and slate tones.

*   **Primary (#567c92):** A muted steel blue used for "Active" states and primary navigation. This represents the structural frame—stable and architectural.
*   **Secondary (#677a86):** A neutral slate reserved for secondary actions and balanced UI components. This provides a bridge between the primary structure and the background.
*   **Tertiary (#6c759e):** A cool periwinkle-slate used for highlights and decorative accents that require subtle distinction without breaking the industrial tone.
*   **Surface Hierarchy:** 
    *   `surface`: The foundation layer, now utilizing a mid-tone neutral gray (#74777a) to reduce visual fatigue and simulate a matte metallic finish.
    *   `surface_container_low`: Used for secondary navigation or background grouping.
    *   `surface_container_highest`: Reserved for the most interactive, "top-level" elements.

### The "No-Line" Rule
Standard UI relies on 1px borders to separate content. This design system **prohibits** the use of solid borders for sectioning. Boundaries must be defined through background color shifts. This creates a more sophisticated, "machined" look where elements appear to be recessed or extruded from a single block of material.

### Signature Textures
To add "soul" to the industrial aesthetic, use subtle linear gradients (10° angle) transitioning from `primary` to `primary_container` for hero actions. For background depth, apply a very subtle `surface_bright` gradient across large empty sections to mimic the way light hits a matte metal surface.

---

## 3. Typography: Mathematical Rigor
We use **Inter** for its neutral, high-readability characteristics. The typography is the primary driver of the system’s "Editorial" feel.

*   **Display & Headlines:** Use `display-lg` and `headline-lg` with a slightly tighter letter-spacing (-0.02em) to give headers an authoritative, "stamped" appearance.
*   **The "Data Monospaced" Effect:** While we use Inter, for numeric values (metrics, coordinates, timestamps), ensure you utilize the `tnum` (tabular figures) OpenType feature. This ensures numbers align vertically in lists, reinforcing the feeling of engineering precision.
*   **Labels:** `label-md` and `label-sm` should be used for metadata. Treat these like technical annotations on a blueprint—small, high-contrast, and always uppercase when used for categories.

---

## 4. Elevation & Depth: Tonal Layering
In this design system, "up" does not mean "shadowed." We convey elevation through the **Layering Principle.**

*   **The Layering Principle:** Depth is achieved by "stacking" the surface tiers. A `surface_container_lowest` panel represents a "recessed" tray, while a `surface_container_highest` element represents a "raised" control surface. 
*   **Ambient Shadows:** Traditional drop shadows are forbidden. If an element must float (e.g., a modal), use an "Ambient Glow." The shadow should have a 32px to 64px blur, 4% opacity, and use the `primary` color tinted into the shadow to simulate light reflecting off a digital surface.
*   **The "Ghost Border" Fallback:** If accessibility requirements demand a container boundary, use the `outline_variant` at **15% opacity**.

---

## 5. Components

### Layout & Spacing
*   **Rhythm:** The system utilizes **Normal (2)** spacing, providing a balanced, breathable layout that allows complex data sets to remain legible without feeling overly dense or excessively sparse.
*   **Roundedness:** Corners are strictly **Subtle (1)**. This ensures that the interface maintains its "Machined" industrial quality, avoiding the "bubbly" look of consumer apps while providing just enough softening to feel modern.

### Buttons
*   **Primary:** Solid `primary_container` with `on_primary_container` text. Corners must strictly use subtle roundedness. No gradients on buttons; keep them flat and functional.
*   **Secondary:** A "Ghost" style. Use `outline` at 20% opacity for the frame, with `primary` text.

### Cards & Data Containers
*   **Rule:** Forbid the use of divider lines.
*   **Structure:** Separate card sections using standard vertical spacing. Use background shifts to define hierarchy within the card.

### Input Fields
*   **Style:** Inputs should feel "embedded." Use `surface_container_lowest` for the field background.
*   **Focus State:** Instead of a thick border, use a 2px "Glow" on the bottom edge only, using the `primary` color.

---

## 6. Do’s and Don’ts

### Do:
*   **Use Intentional Asymmetry:** Align primary data to the left, but place metadata and secondary actions in a slightly offset right-hand column to break the "template" feel.
*   **Embrace Negative Space:** Use the standard spacing (2) to give data "room to breathe." Industrial intelligence is about clarity.
*   **Use Tonal Shifts:** Rely on the `surface_container` tokens to group related items rather than borders.

### Don’t:
*   **Don't use Vibrant Neons:** All accent colors must be "Muted"—the steel blue and slate should feel like matte-finished industrial components.
*   **Don't use Rounded-Full:** Avoid pill-shaped buttons. Stick to the `subtle` corner radius to maintain the structural, "Industrial" feel.
*   **Don't use High-Density layouts:** Avoid dropping to compact spacing unless specifically required for telemetry-heavy screens.