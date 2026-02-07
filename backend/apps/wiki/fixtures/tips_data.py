"""
Curated Hygiene Tips from Reddit r/AskDocs and r/Hygiene communities
Manually curated for quality, safety, and accuracy
"""

TIPS_DATA = [
    # HAND HYGIENE
    {
        "title": "How to wash hands properly for 20 seconds",
        "slug": "how-to-wash-hands-properly-for-20-seconds",
        "description": "Use warm water and soap, scrub all surfaces of hands including backs, between fingers, and under nails for at least 20 seconds. This is most effective way to prevent germ transmission.",
        "category": "Hand Hygiene",
    },
    {
        "title": "How to use hand sanitizer when unavailable",
        "slug": "how-to-use-hand-sanitizer-when-unavailable",
        "description": "When soap and water aren't available, use an alcohol-based hand sanitizer with at least 60% alcohol. Apply enough to cover all hand surfaces and rub until dry.",
        "category": "Hand Hygiene",
    },
    {
        "title": "How to wash hands before eating properly",
        "slug": "how-to-wash-hands-before-eating-properly",
        "description": "Always wash hands thoroughly before handling food, eating, or cooking, and immediately after using bathroom, changing diapers, or handling garbage.",
        "category": "Hand Hygiene",
    },
    {
        "title": "How to clean under fingernails effectively",
        "slug": "how-to-clean-under-fingernails-effectively",
        "description": "Germs accumulate under fingernails. Use a nail brush or scrub under nails during hand washing. Keep nails trimmed short to reduce germ accumulation.",
        "category": "Hand Hygiene",
    },
    {
        "title": "How to dry hands completely after washing",
        "slug": "how-to-dry-hands-completely-after-washing",
        "description": "Moist hands transfer bacteria more easily than dry hands. Use a clean towel or air dry thoroughly. Avoid leaving hands damp after washing.",
        "category": "Hand Hygiene",
    },
    {
        "title": "How to wash hands after touching surfaces",
        "slug": "how-to-wash-hands-after-touching-surfaces",
        "description": "After touching doorknobs, elevator buttons, shared phones, or other high-touch surfaces in public spaces, wash your hands or use sanitizer to prevent germ transfer.",
        "category": "Hand Hygiene",
    },
    # ORAL HYGIENE
    {
        "title": "How to brush teeth twice daily correctly",
        "slug": "how-to-brush-teeth-twice-daily-correctly",
        "description": "Use fluoride toothpaste and a soft-bristled toothbrush. Brush in gentle circular motions for 2 minutes, covering all tooth surfaces. This prevents cavities and gum disease.",
        "category": "Oral Hygiene",
    },
    {
        "title": "How to floss between teeth daily",
        "slug": "how-to-floss-between-teeth-daily",
        "description": "Flossing removes plaque and food particles from between teeth where a toothbrush can't reach. Slide floss gently up and down, following the curve of each tooth.",
        "category": "Oral Hygiene",
    },
    {
        "title": "How to replace toothbrush every 3-4 months",
        "slug": "how-to-replace-toothbrush-every-3-4-months",
        "description": "Toothbrushes wear out and become less effective. Replace your toothbrush or electric toothbrush head every 3-4 months, or sooner if bristles are frayed.",
        "category": "Oral Hygiene",
    },
    {
        "title": "How to clean tongue scraper properly",
        "slug": "how-to-clean-tongue-scraper-properly",
        "description": "Bacteria accumulate on the tongue causing bad breath. Use a tongue scraper or brush your tongue gently with your toothbrush to remove coating and bacteria.",
        "category": "Oral Hygiene",
    },
    {
        "title": "How to use mouthwash for bacteria",
        "slug": "how-to-use-mouthwash-for-bacteria",
        "description": "Antiseptic mouthwash helps reduce plaque, gingivitis, and bad breath. Swish for 30 seconds and don't eat or drink for 30 minutes after use. Don't replace brushing/flossing.",
        "category": "Oral Hygiene",
    },
    {
        "title": "How to visit dentist every 6 months",
        "slug": "how-to-visit-dentist-every-6-months",
        "description": "Regular dental checkups and cleanings are essential. Dentists can detect problems early and professionally remove tartar that brushing can't eliminate.",
        "category": "Oral Hygiene",
    },
    {
        "title": "How to limit sugary foods for teeth",
        "slug": "how-to-limit-sugary-foods-for-teeth",
        "description": "Sugar feeds bacteria that cause tooth decay. Limit sugary snacks, sodas, and juices. When you do consume them, brush or rinse mouth with water afterward.",
        "category": "Oral Hygiene",
    },
    # SHOWER & BODY HYGIENE
    {
        "title": "How to shower daily or every other day",
        "slug": "how-to-shower-daily-or-every-other-day",
        "description": "Most people benefit from daily or every-other-day showers to remove sweat, dead skin cells, and bacteria. Adjust based on activity level and skin type.",
        "category": "Body Hygiene",
    },
    {
        "title": "How to use lukewarm water for showers",
        "slug": "how-to-use-lukewarm-water-for-showers",
        "description": "Hot water strips natural oils from skin. Use lukewarm water to preserve skin's moisture barrier and prevent dryness and irritation.",
        "category": "Body Hygiene",
    },
    {
        "title": "How to use mild fragrance-free soap",
        "slug": "how-to-use-mild-fragrance-free-soap",
        "description": "Choose gentle, pH-balanced soaps. Avoid harsh antibacterial soaps that can disrupt skin microbiome. Focus on odor-prone areas: underarms, groin, and feet.",
        "category": "Body Hygiene",
    },
    {
        "title": "How to wash feet between toes properly",
        "slug": "how-to-wash-feet-between-toes-properly",
        "description": "Feet accumulate moisture and bacteria. Wash between toes during every shower and dry completely to prevent athlete's foot and fungal infections.",
        "category": "Body Hygiene",
    },
    {
        "title": "How to moisturize skin after showering",
        "slug": "how-to-moisturize-skin-after-showering",
        "description": "Apply moisturizer within 3 minutes of showering while skin is still damp. This locks in hydration and prevents dry, itchy skin.",
        "category": "Body Hygiene",
    },
    {
        "title": "How to exfoliate 1-2 times per week",
        "slug": "how-to-exfoliate-1-2-times-per-week",
        "description": "Use a gentle body scrub or washcloth to remove dead skin cells 1-2 times weekly. Don't over-exfoliate as this can damage skin barrier.",
        "category": "Body Hygiene",
    },
    {
        "title": "How to wear clean underwear daily",
        "slug": "how-to-wear-clean-underwear-daily",
        "description": "Change underwear every day, and after sweating. This prevents bacterial growth, odor, and infections in sensitive areas.",
        "category": "Body Hygiene",
    },
    {
        "title": "How to change socks daily properly",
        "slug": "how-to-change-socks-daily-properly",
        "description": "Wear clean socks every day, and change immediately if they get wet or sweaty. This prevents foot odor and fungal infections.",
        "category": "Body Hygiene",
    },
    # FACIAL HYGIENE
    {
        "title": "How to wash face morning and night",
        "slug": "how-to-wash-face-morning-and-night",
        "description": "Use a gentle cleanser suited to your skin type twice daily. Nighttime washing removes makeup, pollution, and sebum that accumulated during day.",
        "category": "Facial Hygiene",
    },
    {
        "title": "How to avoid over-washing your face",
        "slug": "how-to-avoid-over-washing-your-face",
        "description": "More than twice daily can strip oils and cause irritation. Be gentle - don't scrub hard as this can damage skin barrier.",
        "category": "Facial Hygiene",
    },
    {
        "title": "How to use sunscreen daily correctly",
        "slug": "how-to-use-sunscreen-daily-correctly",
        "description": "Apply broad-spectrum SPF 30+ sunscreen every morning, even on cloudy days. This prevents skin cancer, premature aging, and sun damage.",
        "category": "Facial Hygiene",
    },
    {
        "title": "How to remove makeup before bed",
        "slug": "how-to-remove-makeup-before-bed",
        "description": "Never sleep in makeup. It clogs pores, leads to breakouts, and can cause eye infections. Use a gentle makeup remover or cleanser.",
        "category": "Facial Hygiene",
    },
    {
        "title": "How to avoid touching your face",
        "slug": "how-to-avoid-touching-your-face",
        "description": "Touching your face transfers bacteria and dirt from hands to skin, causing acne and infections. Be mindful of this habit throughout day.",
        "category": "Facial Hygiene",
    },
    {
        "title": "How to stop popping pimples safely",
        "slug": "how-to-stop-popping-pimples-safely",
        "description": "Picking or popping pimples spreads bacteria, causes scarring, and can lead to infection. Let them heal naturally or use spot treatment.",
        "category": "Facial Hygiene",
    },
    {
        "title": "How to change pillowcase weekly",
        "slug": "how-to-change-pillowcase-weekly",
        "description": "Pillowcases accumulate oil, dead skin cells, and bacteria. Wash or change pillowcases at least weekly to prevent breakouts and skin irritation.",
        "category": "Facial Hygiene",
    },
    # HAIR HYGIENE
    {
        "title": "How to wash hair 2-3 times weekly",
        "slug": "how-to-wash-hair-2-3-times-weekly",
        "description": "Most people benefit from washing hair 2-3 times weekly. Over-washing strips natural oils, under-washing can cause buildup. Adjust based on hair type and activity.",
        "category": "Hair Hygiene",
    },
    {
        "title": "How to apply conditioner on ends",
        "slug": "how-to-apply-conditioner-on-ends",
        "description": "Apply conditioner primarily to mid-lengths and ends of hair, not scalp. This moisturizes without weighing hair down or making it greasy.",
        "category": "Hair Hygiene",
    },
    {
        "title": "How to wash hair without hot water",
        "slug": "how-to-wash-hair-without-hot-water",
        "description": "Hot water strips natural oils and can damage hair. Use lukewarm water and finish with a cool rinse to seal cuticles and add shine.",
        "category": "Hair Hygiene",
    },
    {
        "title": "How to wash hairbrush regularly",
        "slug": "how-to-wash-hairbrush-regularly",
        "description": "Hairbrushes accumulate product buildup, oil, and dead skin. Clean them every 1-2 weeks by removing hair and washing with mild shampoo.",
        "category": "Hair Hygiene",
    },
    {
        "title": "How to avoid sharing hair tools",
        "slug": "how-to-avoid-sharing-hair-tools",
        "description": "Sharing brushes, combs, or hair accessories can spread lice, fungi, and bacteria. Keep personal hair tools private.",
        "category": "Hair Hygiene",
    },
    {
        "title": "How to air dry hair properly",
        "slug": "how-to-air-dry-hair-properly",
        "description": "Heat from blow dryers damages hair over time. Air dry when possible, or use heat protectant and lower heat settings when styling.",
        "category": "Hair Hygiene",
    },
    # NAIL HYGIENE
    {
        "title": "How to keep nails short and clean",
        "slug": "how-to-keep-nails-short-and-clean",
        "description": "Short nails are easier to keep clean and harbor fewer bacteria. Trim regularly and clean under nails during hand washing.",
        "category": "Nail Hygiene",
    },
    {
        "title": "How to stop biting your nails",
        "slug": "how-to-stop-biting-your-nails",
        "description": "Nail biting transfers bacteria from hands to mouth, damages nails and cuticles, and can spread infection. Use bitter polish or other deterrents if needed.",
        "category": "Nail Hygiene",
    },
    {
        "title": "How to push back cuticles gently",
        "slug": "how-to-push-back-cuticles-gently",
        "description": "Cut cuticles after showering when soft. Use a cuticle pusher gently, never cut them as they protect nails from infection.",
        "category": "Nail Hygiene",
    },
    {
        "title": "How to clean nail tools properly",
        "slug": "how-to-clean-nail-tools-properly",
        "description": "Clippers, files, and other tools accumulate bacteria. Clean with alcohol or soap after each use to prevent spreading infections.",
        "category": "Nail Hygiene",
    },
    {
        "title": "How to avoid sharing nail tools",
        "slug": "how-to-avoid-sharing-nail-tools",
        "description": "Sharing nail tools spreads fungi, bacteria, and viruses. Keep personal tools for yourself to prevent infections like fungal nail infections.",
        "category": "Nail Hygiene",
    },
    # INTIMATE HYGIENE
    {
        "title": "How to wash genital area properly",
        "slug": "how-to-wash-genital-area-properly",
        "description": "Use only mild, fragrance-free soap on external genital areas. Avoid getting soap inside the vagina as this disrupts natural pH and flora.",
        "category": "Intimate Hygiene",
    },
    {
        "title": "How to wipe front to back properly",
        "slug": "how-to-wipe-front-to-back-properly",
        "description": "Always wipe from front to back after using the toilet to prevent spreading bacteria from anus to urethra and vagina, which can cause infections.",
        "category": "Intimate Hygiene",
    },
    {
        "title": "How to change menstrual products regularly",
        "slug": "how-to-change-menstrual-products-regularly",
        "description": "Change tampons every 4-8 hours and pads every 3-4 hours. Never leave tampons in overnight. This prevents toxic shock syndrome and bacterial growth.",
        "category": "Intimate Hygiene",
    },
    {
        "title": "How to wear breathable underwear properly",
        "slug": "how-to-wear-breathable-underwear-properly",
        "description": "Choose cotton underwear which allows air circulation and reduces moisture. Avoid synthetic materials that trap moisture and promote bacterial/fungal growth.",
        "category": "Intimate Hygiene",
    },
    {
        "title": "How to avoid douching properly",
        "slug": "how-to-avoid-douching-properly",
        "description": "Douching and feminine sprays disrupt natural vaginal balance and can increase infection risk. The vagina is self-cleaning and doesn't require internal cleaning.",
        "category": "Intimate Hygiene",
    },
    {
        "title": "How to practice safe sex hygiene",
        "slug": "how-to-practice-safe-sex-hygiene",
        "description": "Use protection, urinate after sex to flush bacteria, and wash genitals before and after sexual activity to prevent urinary tract and sexually transmitted infections.",
        "category": "Intimate Hygiene",
    },
    # ENVIRONMENTAL HYGIENE
    {
        "title": "How to clean phone screen properly",
        "slug": "how-to-clean-phone-screen-properly",
        "description": "Phones carry more bacteria than toilet seats. Clean daily with alcohol wipe or phone-safe disinfectant, especially after using it in bathrooms or public spaces.",
        "category": "Environmental Hygiene",
    },
    {
        "title": "How to wash bed sheets weekly",
        "slug": "how-to-wash-bed-sheets-weekly",
        "description": "Sheets accumulate sweat, dead skin cells, and allergens. Wash in hot water weekly, especially if you have allergies or acne-prone skin.",
        "category": "Environmental Hygiene",
    },
    {
        "title": "How to disinfect high-touch surfaces daily",
        "slug": "how-to-disinfect-high-touch-surfaces-daily",
        "description": "Clean doorknobs, light switches, remotes, and handles daily during flu season or if someone is sick. Use disinfectant spray or wipes.",
        "category": "Environmental Hygiene",
    },
    {
        "title": "How to ventilate your home daily",
        "slug": "how-to-ventilate-your-home-daily",
        "description": "Open windows for 10-15 minutes daily to improve air circulation and reduce indoor pollutants, mold, and virus concentrations.",
        "category": "Environmental Hygiene",
    },
    {
        "title": "How to clean toilet bowl regularly",
        "slug": "how-to-clean-toilet-bowl-regularly",
        "description": "Clean toilet bowl, seat, and handle with disinfectant at least weekly. Pay attention to hinges and undersides where bacteria hide.",
        "category": "Environmental Hygiene",
    },
    {
        "title": "How to wash towels after 3-4 uses",
        "slug": "how-to-wash-towels-after-3-4-uses",
        "description": "Towels accumulate bacteria and moisture. Wash in hot water after 3-4 uses or sooner if they smell musty. Don't share towels.",
        "category": "Environmental Hygiene",
    },
    # SLEEP HYGIENE
    {
        "title": "How to maintain consistent sleep schedule",
        "slug": "how-to-maintain-consistent-sleep-schedule",
        "description": "Go to bed and wake up at the same time every day, even on weekends. This regulates your body clock and improves sleep quality.",
        "category": "Sleep Hygiene",
    },
    {
        "title": "How to create dark bedroom for sleep",
        "slug": "how-to-create-dark-bedroom-for-sleep",
        "description": "Keep bedroom temperature around 65-68°F (18-20°C) and use blackout curtains or eye mask. Dark, cool environments promote restful sleep.",
        "category": "Sleep Hygiene",
    },
    {
        "title": "How to avoid screens before bed",
        "slug": "how-to-avoid-screens-before-bed",
        "description": "Stop using phones, tablets, and computers 1-2 hours before bed. Blue light suppresses melatonin production and disrupts sleep cycles.",
        "category": "Sleep Hygiene",
    },
    {
        "title": "How to limit caffeine after 2 pm",
        "slug": "how-to-limit-caffeine-after-2-pm",
        "description": "Caffeine stays in your system for 6-8 hours. Avoid coffee, tea, and energy drinks in the afternoon and evening to prevent sleep disruption.",
        "category": "Sleep Hygiene",
    },
    {
        "title": "How to establish bedtime routine",
        "slug": "how-to-establish-bedtime-routine",
        "description": "Create a relaxing pre-sleep routine: reading, light stretching, or meditation. This signals to your body it's time to wind down.",
        "category": "Sleep Hygiene",
    },
    {
        "title": "How to replace pillows every 1-2 years",
        "slug": "how-to-replace-pillows-every-1-2-years",
        "description": "Pillows accumulate dust mites, dead skin, and allergens. Replace every 1-2 years or use hypoallergenic covers to reduce exposure.",
        "category": "Sleep Hygiene",
    },
    # FOOD HYGIENE
    {
        "title": "How to wash hands before food prep",
        "slug": "how-to-wash-hands-before-food-prep",
        "description": "Always wash hands thoroughly with soap and water for 20 seconds before preparing food, after handling raw meat, and between different food types.",
        "category": "Food Hygiene",
    },
    {
        "title": "How to separate raw and cooked foods",
        "slug": "how-to-separate-raw-and-cooked-foods",
        "description": "Use separate cutting boards and utensils for raw meat and ready-to-eat foods. Never place cooked food on surfaces that held raw meat.",
        "category": "Food Hygiene",
    },
    {
        "title": "How to cook meat to safe temperatures",
        "slug": "how-to-cook-meat-to-safe-temperatures",
        "description": "Use a food thermometer to ensure meats reach safe internal temperatures: 165°F (74°C) for poultry, 145°F (63°C) for whole cuts of meat.",
        "category": "Food Hygiene",
    },
    {
        "title": "How to refrigerate perishable food promptly",
        "slug": "how-to-refrigerate-perishable-food-promptly",
        "description": "Don't leave perishable food at room temperature for more than 2 hours (1 hour in hot weather). Refrigerate promptly to prevent bacterial growth.",
        "category": "Food Hygiene",
    },
    {
        "title": "How to wash produce before eating",
        "slug": "how-to-wash-produce-before-eating",
        "description": "Rinse fruits and vegetables under running water, even those with rinds you don't eat. Remove outer leaves of lettuce and cabbage.",
        "category": "Food Hygiene",
    },
    {
        "title": "How to clean kitchen surfaces daily",
        "slug": "how-to-clean-kitchen-surfaces-daily",
        "description": "Wipe counters, cutting boards, and tables with hot soapy water after each use. Sanitize weekly with a bleach solution to kill bacteria.",
        "category": "Food Hygiene",
    },
    # TRAVEL HYGIENE
    {
        "title": "How to use bottled water traveling",
        "slug": "how-to-use-bottled-water-traveling",
        "description": "When traveling to areas with uncertain water quality, use sealed bottled water for drinking and brushing teeth. Avoid ice in drinks.",
        "category": "Travel Hygiene",
    },
    {
        "title": "How to clean airplane tray tables",
        "slug": "how-to-clean-airplane-tray-tables",
        "description": "Airplane tray tables harbor bacteria. Use disinfecting wipes to clean your tray table, armrests, and seatbelt buckle when flying.",
        "category": "Travel Hygiene",
    },
    {
        "title": "How to pack travel-sized hygiene kit",
        "slug": "how-to-pack-travel-sized-hygiene-kit",
        "description": "Carry travel-sized hand sanitizer, tissues, wet wipes, and antibacterial gel. Use hand sanitizer frequently when soap isn't available.",
        "category": "Travel Hygiene",
    },
    {
        "title": "How to wear flip-flops in shared showers",
        "slug": "how-to-wear-flip-flops-in-shared-showers",
        "description": "In gyms, hostels, or hotels, always wear flip-flops in shared showers to prevent athlete's foot and other fungal infections.",
        "category": "Travel Hygiene",
    },
]

CATEGORIES = [
    "Hand Hygiene",
    "Oral Hygiene",
    "Body Hygiene",
    "Facial Hygiene",
    "Hair Hygiene",
    "Nail Hygiene",
    "Intimate Hygiene",
    "Environmental Hygiene",
    "Sleep Hygiene",
    "Food Hygiene",
    "Travel Hygiene",
]
