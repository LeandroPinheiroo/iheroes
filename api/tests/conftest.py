from hypothesis import settings as hypo_settings

from iheroes_api.config.environment import get_settings

settings = get_settings()


# Configure Hypothesis
hypo_settings.register_profile("development", max_examples=10)
hypo_settings.get_profile(settings.HYPOTHESIS_PROFILE)
