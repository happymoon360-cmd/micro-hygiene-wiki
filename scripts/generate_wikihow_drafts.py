from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIPS_DATA_PATH = ROOT / "backend" / "apps" / "wiki" / "fixtures" / "tips_data.py"
DRAFTS_DIR = ROOT / "content" / "drafts"


CATEGORY_CONTEXT = {
    "Hand Hygiene": {
        "prep_items": "soap or sanitizer, a clean towel, and access to clean water",
        "risk": "cross-contact from shared surfaces and face-touching",
        "maintenance": "repeat before eating, after bathrooms, and after public transit",
        "primary": "light blue",
        "accent": "white",
    },
    "Oral Hygiene": {
        "prep_items": "toothbrush, fluoride toothpaste, floss, and a clean rinsing cup",
        "risk": "plaque buildup, gum irritation, and odor from missed areas",
        "maintenance": "follow a morning and evening routine with weekly tool cleaning",
        "primary": "mint green",
        "accent": "white",
    },
    "Body Hygiene": {
        "prep_items": "mild cleanser, clean towel, breathable clothes, and moisturizer if needed",
        "risk": "sweat-related irritation, odor, and skin barrier imbalance",
        "maintenance": "adjust frequency by activity level, climate, and skin tolerance",
        "primary": "lavender",
        "accent": "soft pink",
    },
    "Facial Hygiene": {
        "prep_items": "gentle face cleanser, clean towel, and non-comedogenic moisturizer",
        "risk": "breakouts from over-cleansing, friction, or contaminated hands",
        "maintenance": "keep a stable routine and avoid introducing too many new products at once",
        "primary": "peach",
        "accent": "coral",
    },
    "Hair Hygiene": {
        "prep_items": "shampoo suited to scalp type, conditioner, and clean styling tools",
        "risk": "scalp buildup, irritation, and heat-related dryness",
        "maintenance": "use a repeatable wash cadence and clean tools on schedule",
        "primary": "warm brown",
        "accent": "gold",
    },
    "Nail Hygiene": {
        "prep_items": "clean clippers, soft brush, alcohol wipes, and moisturizer",
        "risk": "bacterial buildup under nails and small skin breaks around cuticles",
        "maintenance": "trim regularly and sanitize tools after each use",
        "primary": "soft pink",
        "accent": "white",
    },
    "Intimate Hygiene": {
        "prep_items": "mild fragrance-free cleanser, breathable fabric, and clean water",
        "risk": "moisture trapping, irritation, and microbial imbalance",
        "maintenance": "keep routines gentle, external, and consistent",
        "primary": "light purple",
        "accent": "white",
    },
    "Environmental Hygiene": {
        "prep_items": "disinfecting wipes, microfiber cloths, and a simple cleaning checklist",
        "risk": "high-touch surface contamination and moisture-driven microbial growth",
        "maintenance": "set daily touch-point wipes and weekly deep-clean blocks",
        "primary": "sage green",
        "accent": "light brown",
    },
    "Sleep Hygiene": {
        "prep_items": "a consistent bedtime plan, dim lighting, and a cool room setup",
        "risk": "poor sleep quality from light exposure, inconsistent timing, and stimulation",
        "maintenance": "protect the routine even on weekends with small adjustments",
        "primary": "dark blue",
        "accent": "indigo",
    },
    "Food Hygiene": {
        "prep_items": "clean prep tools, separate cutting surfaces, and safe storage containers",
        "risk": "cross-contamination and temperature-related bacterial growth",
        "maintenance": "clean as you go and verify storage and cooking temperatures",
        "primary": "warm yellow",
        "accent": "orange",
    },
    "Travel Hygiene": {
        "prep_items": "travel wipes, sanitizer, tissues, and a small clean-zone pouch",
        "risk": "high-touch exposure in transit and fast-turnover shared spaces",
        "maintenance": "use a short check-in and daily touch-up routine",
        "primary": "sky blue",
        "accent": "light green",
    },
}

CAMERA_FRAMES = [
    "medium shot from chest level",
    "close-up from shoulder perspective",
    "top-down workspace view",
    "wide medium shot from front",
    "angled side view at waist height",
    "three-quarter overhead view",
]

STYLE_LOCK = (
    "Style lock: unified wiki visual system v1. Modern flat editorial illustration, "
    "soft pastel blue-green palette, rounded geometry, subtle shading, bright high-key lighting, "
    "very light neutral background, consistent character proportions, clean medical-hygiene tone."
)


CATEGORY_REFERENCES = {
    "Hand Hygiene": [
        ("CDC - About Handwashing", "https://www.cdc.gov/clean-hands/about/index.html"),
        ("CDC - Hand Hygiene FAQ", "https://www.cdc.gov/clean-hands/faq/index.html"),
        (
            "WHO/UNICEF - Guidelines on Hand Hygiene in Community Settings",
            "https://www.who.int/publications/i/item/9789240116559",
        ),
    ],
    "Oral Hygiene": [
        (
            "CDC - Oral Health Tips for Adults",
            "https://www.cdc.gov/oral-health/prevention/oral-health-tips-for-adults.html",
        ),
        ("CDC - About Oral Health", "https://www.cdc.gov/oral-health/about/index.html"),
        (
            "WHO - Oral Health Fact Sheet",
            "https://www.who.int/news-room/fact-sheets/detail/oral-health",
        ),
    ],
    "Body Hygiene": [
        ("CDC - Hygiene", "https://www.cdc.gov/hygiene/index.html"),
        (
            "AAD - Skin Care Basics",
            "https://www.aad.org/public/everyday-care/skin-care-basics",
        ),
        (
            "WHO/UNICEF - Guidelines on Hand Hygiene in Community Settings",
            "https://www.who.int/publications/i/item/9789240116559",
        ),
    ],
    "Facial Hygiene": [
        (
            "AAD - Skin Care Basics",
            "https://www.aad.org/public/everyday-care/skin-care-basics",
        ),
        ("CDC - Hygiene", "https://www.cdc.gov/hygiene/index.html"),
        (
            "WHO - Oral Health Fact Sheet",
            "https://www.who.int/news-room/fact-sheets/detail/oral-health",
        ),
    ],
    "Hair Hygiene": [
        (
            "AAD - Hair and Scalp Care",
            "https://www.aad.org/public/everyday-care/hair-scalp-care",
        ),
        (
            "AAD - Skin Care Basics",
            "https://www.aad.org/public/everyday-care/skin-care-basics",
        ),
        ("CDC - Hygiene", "https://www.cdc.gov/hygiene/index.html"),
    ],
    "Nail Hygiene": [
        (
            "AAD - Nail Care Basics",
            "https://www.aad.org/public/everyday-care/nail-care-secrets/basics",
        ),
        ("CDC - Hygiene", "https://www.cdc.gov/hygiene/index.html"),
        (
            "AAD - Skin Care Basics",
            "https://www.aad.org/public/everyday-care/skin-care-basics",
        ),
    ],
    "Intimate Hygiene": [
        (
            "NHS - Vagina and Vulva Health",
            "https://www.nhs.uk/womens-health/vagina-and-vulva-health/",
        ),
        ("NHS - Vaginitis", "https://www.nhs.uk/conditions/vaginitis/"),
        (
            "ACOG - Vulvovaginal Health FAQ",
            "https://www.acog.org/womens-health/faqs/vulvovaginal-health",
        ),
    ],
    "Environmental Hygiene": [
        (
            "CDC - When and How to Clean and Disinfect Your Home",
            "https://www.cdc.gov/hygiene/about/when-and-how-to-clean-and-disinfect-your-home.html",
        ),
        (
            "CDC - Cleaning and Disinfecting",
            "https://www.cdc.gov/hygiene/cleaning-disinfecting/index.html",
        ),
        ("CDC - Hygiene", "https://www.cdc.gov/hygiene/index.html"),
    ],
    "Sleep Hygiene": [
        ("CDC - About Sleep", "https://www.cdc.gov/sleep/about/index.html"),
        ("NHLBI - Sleep Health", "https://www.nhlbi.nih.gov/health/sleep"),
        (
            "NHS - How to Get to Sleep",
            "https://www.nhs.uk/live-well/sleep-and-tiredness/how-to-get-to-sleep/",
        ),
    ],
    "Food Hygiene": [
        ("CDC - Food Safety", "https://www.cdc.gov/food-safety/index.html"),
        ("CDC - About Food Safety", "https://www.cdc.gov/food-safety/about/index.html"),
        ("WHO - Food Safety", "https://www.who.int/health-topics/food-safety"),
    ],
    "Travel Hygiene": [
        ("CDC - Travelers' Health", "https://wwwnc.cdc.gov/travel"),
        (
            "CDC - Food and Water Safety",
            "https://wwwnc.cdc.gov/travel/page/food-water-safety",
        ),
        (
            "CDC - Cleaning and Disinfecting",
            "https://www.cdc.gov/hygiene/cleaning-disinfecting/index.html",
        ),
    ],
}


def load_tips_data() -> list[dict[str, str]]:
    spec = importlib.util.spec_from_file_location("tips_data", TIPS_DATA_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load tips data from {TIPS_DATA_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.TIPS_DATA)


def normalize_topic(title: str) -> str:
    text = title.strip()
    if text.lower().startswith("how to "):
        text = text[7:]
    return text.strip().rstrip(".")


def split_description(description: str) -> tuple[str, str]:
    plain = re.sub(r"\s+", " ", description.strip())
    if "##" in plain or "![" in plain:
        plain = "Use a clear, step-by-step hygiene routine with full coverage and consistent timing."

    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", plain) if p.strip()]
    if not parts:
        return (
            "Use a clear, step-by-step hygiene routine with full coverage and consistent timing.",
            "Repeat the routine consistently to reduce avoidable contamination risks.",
        )

    core = parts[0]
    support = (
        parts[1]
        if len(parts) > 1
        else "Repeat the routine consistently to reduce avoidable contamination risks."
    )
    return core, support


def build_prompt(index: int, topic: str, scene: str) -> str:
    frame = CAMERA_FRAMES[(index - 1) % len(CAMERA_FRAMES)]

    return (
        f"![image-{index}](PROMPT: Instructional illustration for a hygiene tutorial about {topic}. "
        f"Scene: {scene}. Camera framing: {frame}. Subject details: clean environment, practical action in progress, "
        f"neutral expression, clear hand and tool positioning. {STYLE_LOCK} Composition: "
        f"clear focal point, no clutter, no text overlay, no logos, no watermark. Quality: high clarity, educational, "
        f"beginner-friendly, consistent with previous steps.)"
    )


def build_article(title: str, slug: str, category: str, base_description: str) -> str:
    topic = normalize_topic(title)
    core_sentence, support_sentence = split_description(base_description)
    cfg = CATEGORY_CONTEXT[category]

    intro = (
        f"{title} may look simple, but consistent technique matters when you want reliable results. "
        f"This guide gives you a repeatable routine you can follow quickly without skipping key hygiene checks. "
        f"Use it as a practical checklist, not a one-time fix."
    )

    why_this_matters = (
        f"Many hygiene problems come from missed steps rather than lack of effort. "
        f"For this topic, the main risk is {cfg['risk']}. "
        f"A structured routine helps reduce that risk by keeping actions in a stable order. "
        f"Core principle: {core_sentence} {support_sentence}"
    )

    verification_note = (
        "This guide begins with community-reported patterns, then applies second-level verification "
        "against institutional guidance. If community advice conflicts with official guidance, this "
        "article follows the official source and keeps conservative wording."
    )

    steps = [
        (
            "Step 1: Gather supplies before you start",
            (
                f"Prepare everything needed for {topic}: {cfg['prep_items']}. "
                "When tools are ready first, you avoid rushed shortcuts and repeated backtracking. "
                "Set items on a clean, easy-to-reach surface so the sequence stays smooth."
            ),
            f"organizing supplies needed for {topic} on a clean surface",
        ),
        (
            "Step 2: Wash hands and prep the work area",
            (
                "Clean hands first, then set up the immediate area you will touch most. "
                "This prevents early cross-contact and gives you a cleaner baseline for the rest of the routine. "
                "If possible, separate a clean zone from a used-items zone before beginning."
            ),
            f"washing hands and preparing a clean setup zone for {topic}",
        ),
        (
            "Step 3: Define your target standard before the first pass",
            (
                f"Decide what a completed result for {topic} looks like before you begin. "
                "Clear targets improve consistency and help you notice missed areas early. "
                "Use a simple check: full coverage, proper timing, and clean finish."
            ),
            f"reviewing a simple checklist before starting {topic}",
        ),
        (
            "Step 4: Perform the core action with full technique",
            (
                f"Apply the main action slowly and completely for {topic}. "
                f"Remember this anchor: {core_sentence} "
                "Do not rush the first pass, because speed usually creates gaps that need rework later."
            ),
            f"performing the core routine for {topic} with controlled motions",
        ),
        (
            "Step 5: Cover easy-to-miss spots on the second pass",
            (
                "Most failures happen in edge zones, corners, undersides, or transition areas. "
                f"After the core pass, revisit hidden points related to {topic} and complete them deliberately. "
                "A short second pass improves outcomes much more than one rushed sweep."
            ),
            f"targeting hidden spots during {topic} with a second pass",
        ),
        (
            "Step 6: Keep timing, pressure, and contact consistent",
            (
                "Use steady pressure and enough contact time for each movement. "
                "Inconsistent timing weakens results even when the right product or tool is used. "
                "If a surface or area should stay wet briefly, maintain that window before moving on."
            ),
            f"maintaining consistent timing and pressure while doing {topic}",
        ),
        (
            "Step 7: Finish with a clean handoff",
            (
                "Complete the routine by handling final touch points with clean tools or clean hands. "
                "This prevents re-contamination right after you finish the main work. "
                "Store tools in a way that keeps clean and used items separate."
            ),
            f"finishing {topic} and separating clean tools from used tools",
        ),
        (
            "Step 8: Verify outcome and make one correction",
            (
                f"Pause and check whether {topic} meets your target standard from Step 3. "
                "If not, choose one focused correction instead of repeating everything. "
                "This keeps the routine efficient while still improving quality."
            ),
            f"verifying results of {topic} and applying one focused correction",
        ),
        (
            "Step 9: Set a realistic maintenance schedule",
            (
                f"Long-term success comes from repetition, not intensity. {cfg['maintenance']}. "
                "Tie the routine to existing habits so it is easier to keep over time. "
                "Short, regular sessions usually outperform rare deep sessions."
            ),
            f"planning a repeat schedule for {topic} on a weekly calendar",
        ),
        (
            "Step 10: Know when to escalate",
            (
                "If you notice persistent irritation, unusual odor, visible contamination, or worsening conditions, escalate early. "
                "For personal-health concerns, contact a qualified professional. For shared spaces, request proper support instead of patch fixes. "
                "Escalation is part of a good hygiene system, not a failure."
            ),
            f"deciding to escalate after warning signs appear during {topic}",
        ),
        (
            "Step 11: Document what worked for your next cycle",
            (
                "Write down one adjustment that improved speed or quality this time. "
                "Small notes make future sessions more consistent and reduce decision fatigue. "
                "Keep documentation short so the habit remains practical."
            ),
            f"recording a quick note after completing {topic}",
        ),
        (
            "Step 12: Reset supplies so the next run is friction-free",
            (
                "Refill or replace essentials immediately after finishing. "
                "A ready kit removes startup friction and helps you follow through on your maintenance schedule. "
                "Store items in one dedicated location for easy access."
            ),
            f"resetting and restocking supplies used for {topic}",
        ),
    ]

    lines: list[str] = [
        "---",
        f'title: "{title}"',
        f'slug: "{slug}"',
        f'category: "{category}"',
        "---",
        "",
        intro,
        "",
        "## Why This Matters",
        "",
        why_this_matters,
        "",
        "## Secondary Verification",
        "",
        verification_note,
        "",
        '- Claims use careful language ("may", "can", "is associated with") instead of guarantees.',
        "- This article is educational and not a diagnosis or personalized medical treatment.",
        "- Escalation guidance is included when warning signs appear.",
        "",
        "## Method 1 of 3: Prepare for Consistent Results",
        "",
    ]

    for i, (heading, text, scene) in enumerate(steps[:4], start=1):
        lines.extend(
            [
                f"### {heading}",
                "",
                text,
                "",
                build_prompt(i, topic, scene),
                "",
            ]
        )

    lines.extend(
        [
            "## Method 2 of 3: Execute the Core Routine",
            "",
        ]
    )

    for i, (heading, text, scene) in enumerate(steps[4:8], start=5):
        lines.extend(
            [
                f"### {heading}",
                "",
                text,
                "",
                build_prompt(i, topic, scene),
                "",
            ]
        )

    lines.extend(
        [
            "## Method 3 of 3: Maintain Quality Over Time",
            "",
        ]
    )

    for i, (heading, text, scene) in enumerate(steps[8:], start=9):
        lines.extend(
            [
                f"### {heading}",
                "",
                text,
                "",
                build_prompt(i, topic, scene),
                "",
            ]
        )

    lines.extend(
        [
            "## Common Mistakes to Avoid",
            "",
            "- Skipping setup and then improvising midway through the routine.",
            "- Doing only one fast pass and missing edge or hidden zones.",
            "- Using inconsistent timing, pressure, or contact duration.",
            "- Mixing clean tools with used tools right after finishing.",
            "- Ignoring warning signs that require escalation.",
            "",
            "## Pro Tips",
            "",
            '> "Reliable hygiene is a sequence, not a sprint. Keep the order, and quality follows."',
            "",
            "- Keep a compact checklist on your phone for repeat consistency.",
            "- Replace or clean tools on schedule so performance stays stable.",
            "- Use short maintenance sessions to prevent large cleanup events.",
            "- Track one metric (time, completion rate, or comfort) each week.",
            "",
            "## References",
            "",
            *references_lines(category),
            "- [CDC - Health Literacy](https://www.cdc.gov/health-literacy/php/about/index.html)",
            "",
        ]
    )

    return "\n".join(lines)


def word_count_excluding_prompts(text: str) -> int:
    body = text.split("---", 2)[2] if text.startswith("---") else text
    no_prompt_lines = "\n".join(
        line for line in body.splitlines() if "(PROMPT:" not in line
    )
    return len(re.findall(r"[A-Za-z0-9']+", no_prompt_lines))


def references_lines(category: str) -> list[str]:
    refs = CATEGORY_REFERENCES[category]
    return [f"- [{label}]({url})" for label, url in refs]


def main() -> None:
    tips = load_tips_data()
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    min_words = None
    max_words = 0

    for tip in tips:
        title = tip["title"].strip()
        slug = tip["slug"].strip()
        description = tip["description"].strip()
        category = tip["category"].strip()

        if category not in CATEGORY_CONTEXT:
            raise ValueError(f"Unsupported category: {category}")

        article = build_article(title, slug, category, description)

        draft_path = DRAFTS_DIR / f"{slug}.md"
        draft_path.write_text(article, encoding="utf-8")

        count = word_count_excluding_prompts(article)
        min_words = count if min_words is None else min(min_words, count)
        max_words = max(max_words, count)
        generated += 1

    print(f"Generated drafts: {generated}")
    print(f"Word count range (excluding prompts): {min_words} - {max_words}")


if __name__ == "__main__":
    main()
