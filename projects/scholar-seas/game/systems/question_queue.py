class QuestionNode:

    def __init__(self, question):
        self.question = question
        self.next = None


class QuestionQueue:

    def __init__(self):
        self.front = None
        self.back = None
        self.length = 0

    def add(self, question):
        new_node = QuestionNode(question)

        if self.back is None:
            self.front = new_node
            self.back = new_node
        else:
            self.back.next = new_node
            self.back = new_node

        self.length += 1

    def remove(self):
        if self.front is None:
            return None

        question = self.front.question
        self.front = self.front.next
        self.length -= 1

        if self.front is None:
            self.back = None

        return question

    def is_empty(self):
        return self.front is None