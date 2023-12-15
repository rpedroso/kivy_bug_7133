from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.core.window import Window


if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity

    View = autoclass('android.view.View')
    WMLayoutParams = autoclass('android.view.WindowManager$LayoutParams')

    @run_on_ui_thread
    def show_system_bars():
        Logger.info('MyApp: Running show_system_bars()')
        option = (View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_VISIBLE
                )
        window = mActivity.getWindow()
        window.getDecorView().setSystemUiVisibility(option)
        window.addFlags(WMLayoutParams.FLAG_FORCE_NOT_FULLSCREEN)
        window.clearFlags(WMLayoutParams.FLAG_FULLSCREEN)

    @run_on_ui_thread
    def hide_system_bars():
        Logger.info('MyApp: Running hide_system_bars()')
        option = (View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                )

        window = mActivity.getWindow()
        window.getDecorView().setSystemUiVisibility(option)
        window.addFlags(WMLayoutParams.FLAG_FULLSCREEN)
        window.clearFlags(WMLayoutParams.FLAG_FORCE_NOT_FULLSCREEN)


class MyApp(App):

    def build(self):
        self.hide()

        label = Label(text="Hello, World")
        label.on_touch_down = self.on_touch_down

        Window.bind(on_resize=self.on_resize)

        return label

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.hide() if self.has_system_bars else self.show()

    def on_resize(self, *args):
        Logger.info('MyApp: on_resize %r' % (args,))

    def hide(self):
        self.has_system_bars = False
        if platform == 'android':
            hide_system_bars()

    def show(self):
        self.has_system_bars = True
        if platform == 'android':
            show_system_bars()


MyApp().run()
