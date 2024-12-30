from engine.actions import Action


class Test1(Action):
    def perform(self, obj):
        obj.rect.x += 1


class Test2(Action):
    def perform(self, obj):
        obj.rect.x -= 1


class Test3(Action):
    def perform(self, obj):
        obj.rect.y -= 2


class Test4(Action):
    def perform(self, obj):
        obj.rect.y += 1
