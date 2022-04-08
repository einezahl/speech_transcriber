# -*- coding: utf-8 -*-
from enum import Enum, auto

import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer
from testwindow import show_test_window


class RecordingEnum(Enum):
    STARTED = auto()
    STOPPED = auto()


widgets_basic_listbox_item_current = 1
recording_state = RecordingEnum.STOPPED
widget_api_key = "Insert your API key here"


def main():
    global widgets_basic_listbox_item_current
    global recording_state
    global widget_api_key
    imgui.create_context()
    window = impl_glfw_init()
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
            current=widgets_basic_listbox_item_current,
            items=["Hello", "World", "What", "is", "up", "dude?"],
            height_in_items=4,
        )
        if recording_state == RecordingEnum.STOPPED:
            if imgui.button("Start Recording", width=imgui.get_window_width()):
                print("Start Recording")
                recording_state = RecordingEnum.STARTED
        else:
            if imgui.button("Stop Recording", width=imgui.get_window_width()):
                print("Stop Recording")
                recording_state = RecordingEnum.STOPPED
        imgui.button(label="Delete Recording", width=imgui.get_window_width())
        imgui.button(label="Play Recording", width=imgui.get_window_width())
        changed, widget_api_key = imgui.input_text(
            label="Insert your API key here",
            value=widget_api_key,
            buffer_length=400
        )
        imgui.button(label="Transcribe Recording",
                     width=imgui.get_window_width())
        imgui.text("Your transcription should be here")
        imgui.end()

        show_test_window()
        # imgui.show_test_window()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
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


if __name__ == "__main__":
    main()
