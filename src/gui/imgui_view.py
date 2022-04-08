from enum import Enum, auto

import glfw
import OpenGL.GL as gl

import imgui
import imgui.integrations.glfw as GlfwRenderer

from src.gui.controller import Controller


class RecordingEnum(Enum):
    STARTED = auto()
    STOPPED = auto()


class ImguiView:
    def __init__(self, controller, model):
        self.widgets_basic_listbox_item_current = 1
        self.recording_state = RecordingEnum.STOPPED
        self.widget_api_key = "Insert your API key here"
        self.controller = controller
        self.model = model

    def render(self):
        imgui.create_context()
        window = self.impl_glfw_init()
        impl = GlfwRenderer(window)

        while not glfw.window_should_close(window):
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            if imgui.begin_main_menu_bar():
                if imgui.begin_menu("File", True):

                    clicked_quit, selected_quit = imgui.menu_item(
                        "Quit", 'Cmd+Q', False, True
                    )

                    if clicked_quit:
                        exit(1)

                    imgui.end_menu()
                imgui.end_main_menu_bar()

            imgui.begin("Custom window", True)
            imgui.push_item_width(imgui.get_window_width())

            changed, widgets_basic_listbox_item_current = imgui.listbox(
                label='',
                current=self.widgets_basic_listbox_item_current,
                items=self.model.recordings,
                height_in_items=4,
            )
            if self.recording_state == RecordingEnum.STOPPED:
                if imgui.button(
                    "Start Recording",
                    width=imgui.get_window_width()
                ):
                    self.controller.start_recording()
                    self.recording_state = RecordingEnum.STARTED
            else:
                if imgui.button(
                    "Stop Recording",
                    width=imgui.get_window_width()
                ):
                    self.controller.stop_recording()
                    self.recording_state = RecordingEnum.STOPPED
            if imgui.button(
                label="Delete Recording",
                width=imgui.get_window_width()
            ):
                self.controller.delete_recording()
            if imgui.button(
                label="Play Recording",
                width=imgui.get_window_width()
            ):
                self.controller.play_recording()
            changed, self.widget_api_key = imgui.input_text(
                label="Insert your API key here",
                value=self.widget_api_key,
                buffer_length=400
            )
            if self.widget_api_key != "Insert your API key here":
                if imgui.button(
                    label="Transcribe Recording",
                    width=imgui.get_window_width()
                ):
                    self.controller.transcribe_recording(self.widget_api_key)
                    self.transcription =
            imgui.text("Your transcription should be here")
            imgui.end()

            gl.glClearColor(1., 1., 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            impl.render(imgui.get_draw_data())
            glfw.swap_buffers(window)

        impl.shutdown()
        glfw.terminate()
        imgui.end()

    def impl_glfw_init(self):
        width, height = 1280, 720
        window_name = "minimal ImGui/GLFW3 example"

        if not glfw.init():
            print("Could not initialize OpenGL context")
            exit(1)

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

        # Create a windowed mode window and its OpenGL context
        window = glfw.create_window(
            int(width), int(height), window_name, None, None
        )
        glfw.make_context_current(window)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            exit(1)

        return window
