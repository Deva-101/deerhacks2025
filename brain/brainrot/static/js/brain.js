let SELECTORS = {
    frontal_lobe: '.tdc-frontal-lobe',
    cerebellum: '.tdc-cerebellum',
    occipital_lobe: '.tdc-occipital-lobe',
    parietal_lobe: '.tdc-parietal-lobe',
    temporal_lobe: '.tdc-temporal-lobe',
    brain_stem: '.tdc-brain-stem',
    info_title: '.tdc-info-title',
    info_description: '.tdc-info-description',
    filter_container: '.tdc-main-right-filter'
};

let info = {
    brain: {
        frontal_lobe: {
            'selector': SELECTORS.frontal_lobe,
            'title': 'Frontal Lobe',
            'description': 'The Frontal Lobe is the most recently-evolved part of the brain and the last to develop in young adulthood. It\'s dorso-lateral prefrontal circuit is the brain\'s top executive. <br> <br> It organizes responses to complex problems, plans steps to an objective, searches memory for relevant experience, adapts strategies to accommodate new data, guides behavior with verbal skills and houses working memory.',
            'highlight': ['planning', 'motor_functions', 'higher_order_functions',
                'reasoning', 'judgement', 'impulse_control', 'memory',
                'language'
            ]
        },
        cerebellum: {
            'selector': SELECTORS.cerebellum,
            'title': 'Cerebellum',
            'description': 'Two peach-size mounds of folded tissue located at the top of the brain stem, the cerebellum is the guru of skilled, coordinated movement and is involved in some learning pathways.',
            'highlight': ['fine_movement_coordination', 'balance_and_equilibrium',
                'muscle_tone', 'sense_of_body_position'
            ]
        },
        occipital_lobe: {
            'selector': SELECTORS.occipital_lobe,
            'title': 'Occipital Lobe',
            'description': 'The Occipital Lobe processes visual data and routes it to other parts of the brain for identification and storage.',
            'highlight': ['visual_perception', 'color_recognition', 'reading',
                'reading_comprehension', 'depth_perception',
                'recognition_of_object_movement'
            ]
        },
        parietal_lobe: {
            'selector': SELECTORS.parietal_lobe,
            'title': 'Parietal Lobe',
            'description': 'The Parietal Lobe receives and processes sensory information from the body including calculating location and speed of objects.',
            'highlight': ['cognition', 'information_processing', 'touch_sensation',
                'understanding_spatial_orientation', 'movement_coordination',
                'speech', 'visual_perception', 'reading', 'writing',
                'mathematical_computation'
            ]
        },
        temporal_lobe: {
            'selector': SELECTORS.temporal_lobe,
            'title': 'Temporal Lobe',
            'description': 'The Temporal Lobe controls memory storage area, emotion, hearing, and, on the left side, language.',
            'highlight': ['auditory_perception', 'memory', 'speech', 'language_comprehension',
                'emotional_responses', 'visual_perception', 'facial_recognition'
            ]
        },
        brain_stem: {
            'selector': SELECTORS.brain_stem,
            'title': 'Brain Stem',
            'description': 'The part of the brain that connects to the spinal cord. The brain stem controls functions basic to the survival of all animals, such as heart rate, breathing, digesting foods, and sleeping.',
            'highlight': ['alertness', 'arousal', 'breathing', 'blood_pressure',
                'digestion', 'heart_rate'
            ]
        }
    }
};

function setActivePart(regionId) {
    // Convert from kebab-case to snake_case
    const regionKey = regionId.replace('-', '_');

    // Get the brain part info
    const part = info.brain[regionKey];
    if (!part) return;

    // Clear all active states
    $('.tdc-brain-part').removeClass('active');

    // Set the active brain part
    $(part.selector).addClass('active');

    // Update the information panel
    $(SELECTORS.info_title).html(part.title);
    $(SELECTORS.info_description).html(part.description);

    // Add function items if they don't exist
    if ($(SELECTORS.filter_container).is(':empty')) {
        let functionsItems = '';
        _.each(part.highlight, func => {
            functionsItems += `<div class="tdc-main-right-filter-item item-${func} ${regionKey} active">${func.replace(/\_/g, ' ')}</div>`;
        });
        $(SELECTORS.filter_container).html(functionsItems);
    }
}

// Initialize when document is ready
$(document).ready(() => {
    // Get the region from Django
    const regionFromDjango = $('#brain-region').val().trim();

    if (regionFromDjango) {
        setActivePart(regionFromDjango);
    }
});
