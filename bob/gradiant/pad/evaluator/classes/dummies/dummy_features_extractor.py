from bob.gradiant.core import FeaturesExtractor


class DummyFeaturesExtractor(FeaturesExtractor):

    def run(self, dict_images, annotations = None):
        dict_features = {}
        for key, image in dict_images.items():
            features = image[:10, 1, 1]
            dict_features[key] = features
        return dict_features