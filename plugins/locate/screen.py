import sys
import pygame
import gui_objects
from time import strftime, localtime, time
# from time import time, gmtime, strftime, mktime, localtime
from pprint import pprint
from pygame.locals import K_RETURN, KEYDOWN
from global_variables import COLORS, TITLE_RECT, ROWS
from displayscreen import PiInfoScreen
from database import RACK_DB
sys.dont_write_bytecode = True


# For more information on the variables and functions in this file view
# displayscreen.py in the root folder of this project


class myScreen(PiInfoScreen):
    # PiInfoScreen.__init__()
    refreshtime = 1
    displaytime = 5
    pluginname = "File Accn"
    plugininfo = "place to file things. "
    accn = ''

    def __init__(self, *args, **kwargs):
        PiInfoScreen.__init__(self, args[0], kwargs)

        self.timer = False
        self.timeout = 0
        self.timeout_delay = 5  # in seconds

        self.surface.fill(COLORS['CLOUD'])
        # draw the title background
        self.accn_surface.fill(COLORS['CLOUD'])
        RACK_DB.next_location()
        self.result = []
        self.title = gui_objects.text_label(
            surface=self.title_surface,
            font=self.fonts['title_font']['font'],
            text=self.name,
            color=COLORS[self.fonts['title_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=TITLE_RECT,
            rounded=True,
            background_color=COLORS[self.color])
        # ---------------------------------------------
        # These are hardcoded information labels
        #-----------------------------------------------
        self.hint_rect = pygame.Rect(0, 120, 320, 60)
        self.hint_surface = self.surface.subsurface(self.hint_rect)
        self.hint_text = gui_objects.render_textrect(
            string="scan to locate\nswipe up for keyboard",
            font=self.fonts['swipe_font']['font'],
            rect=self.hint_rect,
            text_color=COLORS[self.color],
            background_color=COLORS['CLOUD'],
            justification=1,
            FontPath=self.fonts['swipe_font']['path'],
            cutoff=False,
            MinFont=self.fonts['swipe_font']['size'] - 3,
            MaxFont=self.fonts['swipe_font']['size'],
            shrink=True,
            vjustification=1)
        # self.hint_surface = self.hint_text.update()

        self.result_rect = pygame.Rect(0, 120, 320, 60)
        self.result_surface = self.surface.subsurface(self.result_rect)
        self.result_text = gui_objects.render_textrect(
            string="",
            font=self.fonts['result_font']['font'],
            rect=self.result_rect,
            text_color=COLORS[self.color],
            background_color=COLORS['CLOUD'],
            justification=1,
            FontPath=self.fonts['result_font']['path'],
            cutoff=False,
            MinFont=self.fonts['result_font']['size'] - 8,
            MaxFont=self.fonts['result_font']['size'],
            shrink=True,
            vjustification=1)

        self.info0_rect = pygame.Rect(5, 93, 310, 25)
        self.info0_surface = self.surface.subsurface(self.info0_rect)
        self.info0 = gui_objects.text_label(
            surface=self.info0_surface,
            font=self.fonts['info_font']['font'],
            text="",
            color=COLORS[self.fonts['info_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info0_rect,
            valign='bottom',
            align="center",
            background_color=COLORS['CLOUD'])

        self.info1_rect = pygame.Rect(5, 210, 310, 20)
        self.info1_surface = self.surface.subsurface(self.info1_rect)
        self.info1 = gui_objects.text_label(
            surface=self.info1_surface,
            font=self.fonts['info_font']['font'],
            text="",
            color=COLORS[self.fonts['info_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info1_rect,
            valign='bottom',
            align="center",
            background_color=COLORS['CLOUD'])

        # ------------------------------------------
        # These information labels will change when the screen is updated
        #----------------------------------------
        self.info2_rect = pygame.Rect(120, 93, 160, 25)
        self.info2_surface = self.surface.subsurface(self.info2_rect)
        self.info2 = gui_objects.text_label(
            surface=self.info2_surface,
            font=self.fonts['default_font']['font'],
            text="",
            color=COLORS[self.fonts['default_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info2_rect,
            valign='bottom',
            fontPath=self.fonts['default_font']['path'],
            align="left",
            background_color=COLORS['CLOUD'])

        self.info3_rect = pygame.Rect(150, 200, 120, 20)
        self.info3_surface = self.surface.subsurface(self.info3_rect)
        self.info3 = gui_objects.text_label(
            surface=self.info3_surface,
            font=self.fonts['default_font']['font'],
            text="",
            color=COLORS[self.fonts['default_font']['color']],
            # Rect(left, top, width, height) -> Rect
            rect=self.info3_rect,
            valign='bottom',
            align="left",
            background_color=COLORS['CLOUD'])
        self.text_objects = [
            self.title,
            self.info0,
            self.info1,
            self.info2,
            self.info3]





        for thing in self.text_objects:
            thing.update()

    def reset(self):
        # self.hint_text.fontsize = self.hint_text.MaxFont
        self.info0.text = ''
        self.result_text.font = self.fonts['result_font']['font']
        self.info1.text = ''
        self.result_text.cutoff = False

    def event_handler(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            accn = self.accn_input.value
            if accn != '':
                self.reset()
                self.timeout = time() + self.timeout_delay
                self.timer = True
                result = RACK_DB.find_accn(accn)
                if not result:
                    self.result_text.string = "not found"
                    self.info0.text = accn

                else:
                    self.info0.text = "Accn #: " + accn
                    self.info1.text = '' if len(
                        result) < 5 else "Showing last 4 locations"
                    self.result_text.string = ''
                    reversed_list = reversed(result[-4:])
                    formated = []
                    for item in reversed_list:
                        formated.append(gui_objects.format_location(item))
                    self.result_text.string = "\n".join(formated)
                    pprint(formated)
                    print self.result_text.string
        self.accn_input.update(event)

    def update_locations(self):
        pass

    def showScreen(self):
        print pygame.mouse.get_pos()
        if self.timer:
            if self.timeout < time():
                self.reset()
                self.timer = False
            else:
                self.result_surface.blit(self.result_text.update(), (0, 0))
        else:
            self.hint_surface.blit(self.hint_text.update(), (0, 0))

        self.clock.text = strftime("%H:%M", localtime(time()))
        self.clock.update()
        self.info0.update()
        self.info1.update()
        self.accn_input.draw(self.surface, self.accn_surface, COLORS['CLOUD'])
        self.screen.blit(self.surface, (0, 0))
        return self.screen
