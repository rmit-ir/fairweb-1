from TopicType.modules.M import M
from TopicType.modules.Y import Y
from TopicType.modules.R import R


class TopicFactory:
    def __init__(self, topic):
        self.topictype = list(topic)[0]

    def create_topic_type_extraction(self):
        if self.topictype == 'R':
            return R()
        elif self.topictype == 'M':
            return M()
        elif self.topictype == 'Y':
            return Y()
        else:
            raise ValueError("Invalid Topic or Topic Type")
