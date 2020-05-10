from .base import Widget


class DetailedList(Widget):
    def create(self):
        self._action('create DetailedList')

    def change_source(self, source):
        self._action('change source', source=source)

    def insert(self, item):
        self._action('insert', item=item)

    def change(self, item):
        self._action('change', item=item)

    def remove(self, item, index):
        self._action('remove', item=item, index=index)

    def clear(self, old_data):
        self._action('clear', old_data=old_data)

    def set_on_refresh(self, handler):
        self._set_value('on_refresh', handler)

    def after_on_refresh(self):
        self._action('after on refresh')

    def set_on_delete(self, handler):
        self._set_value('on_delete', handler)

    def set_on_select(self, handler):
        self._set_value('on_select', handler)

    def scroll_to_row(self, row):
        self._set_value('scroll to', row)
