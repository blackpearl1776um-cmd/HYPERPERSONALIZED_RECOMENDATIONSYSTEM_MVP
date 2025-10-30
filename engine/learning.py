class PreferenceLearner:
    def __init__(self):
        self.learned_weights = {}
        self.interaction_history = []
    
    def initialize_weights(self, tags):
        """Initialize all weights to 1.0 (neutral)"""
        self.learned_weights = {tag: 1.0 for tag in tags}
    
    def track_interaction(self, user_action):
        """
        Track user interactions for learning
        user_action: dict with keys 'action_type', 'product_tags', 'timestamp'
        """
        self.interaction_history.append(user_action)
        self._update_weights(user_action)
    
    def _update_weights(self, user_action):
        """Update learned weights based on user action"""
        action_weights = {
            'view': -0.3,   # - for ignore behaviour
            'click': 0.5,
            'wishlist': 0.8,
            'purchase': 1.5
        }
        
        weight_boost = action_weights.get(user_action['action_type'], 0.1)
        
        for tag in user_action.get('product_tags', []):
            if tag in self.learned_weights:
                self.learned_weights[tag] += weight_boost * 0.3
    
        self._normalize_weights()
    
    def _normalize_weights(self):
        """Keep weights between 0.3 and 2.0"""  # Wider range
        for tag in self.learned_weights:
            self.learned_weights[tag] = max(0.3, min(2.0, self.learned_weights[tag]))
    
    def get_learned_weights(self):
        return self.learned_weights.copy()
    
    def apply_learning_to_score(self, base_score, product_tags):
        adjusted_score = base_score
        for tag in product_tags:
            if tag in self.learned_weights:
                adjusted_score *= self.learned_weights[tag]
        return adjusted_score

learner = PreferenceLearner()