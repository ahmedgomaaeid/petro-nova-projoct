from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import pandas as pd
import numpy as np



df=pd.read_csv(".\Data\Quakes locations.csv")
df_apollo=pd.read_csv(".\Data\Apollo_landing_coordinates.csv")


n=0
flag=[]
seen=[]
while n < len(df):
    flag.append(False)
    seen.append(False)
    n+=1

model = Ursina(development_mode=False)

screen=Entity()
camera.parent=screen
camera.z=-20

paused = True


# create two lists to store the moonquakes and stations entities
global dark_moonquakes, light_moonquakes , dark_stations , light_stations
dark_moonquakes = []
light_moonquakes=[]
dark_stations = []
light_stations=[]


#====== Moonquakes ===========================================================================================================

i=0
while i < len(df):
    Q=Entity(model="quad",enabled=False,scale=df.loc[i]["Magnitude"],origin=(0,0,(3.5/df.loc[i]["Magnitude"])),texture=".\Texture\quakes.png",rotation_x=df.loc[i]["Lat"],rotation_y=df.loc[i]["Long"]*-1)
    LQ=Entity(model="quad",enabled=False,scale=df.loc[i]["Magnitude"],origin=(0,0,(3.5/df.loc[i]["Magnitude"])),texture=".\Texture\quakes.png",rotation_x=df.loc[i]["Lat"],rotation_y=df.loc[i]["Long"]*-1)
    E=Sequence(1,Func(Q.blink,duration=1), loop=True)
    LE=Sequence(1,Func(LQ.blink,duration=1), loop=True)
    E.start() ; LE.start()
    dark_moonquakes.append(Q)
    light_moonquakes.append(LQ)
    i+=1



for lq in light_moonquakes:
    lq.unlit=True

toggle_q = False
# Moon quakes func
def toggle_quakes():
    global toggle_q,track
    if not toggle_q:
        destroy(track)
        track = Audio(sound_file_name='.\Sound\Moonquakes.mp3', volume=30)
        n=0
        while n < len(flag):
            flag[n]=True
            n+=1
        if not light_state:
            for q in dark_moonquakes:
                q.texture='.\Texture\quakes.png'
                q.enabled=True
        else:
            for lq in light_moonquakes:
                lq.texture='.\Texture\quakes.png'
                lq.enabled=True
        toggle_q = True
    else:
        destroy(track)
        n=0
        while n < len(flag):
            flag[n]=False
            seen[n]=False
            n+=1
        for lq in light_moonquakes:
            lq.texture='.\Texture\quakes.png'
            lq.enabled=False
        for q in dark_moonquakes:
            q.texture='.\Texture\quakes.png'
            q.enabled=False
        toggle_q = False
        destroy(current_text)


        

Q=Button(color=color.light_gray,scale=(.2,.2),origin=(3.7,.7),texture=".\Texture\Quakes B.jpg")
Q.tooltip=Tooltip("This will show the places of MoonQuakes")
Q.on_click = toggle_quakes
#=================================================================================================================








#====== APOLLO stattions ===========================================================================================================

i = 0
while i < len(df_apollo):
    L = Entity(model="quad",enabled=False,texture=df_apollo.loc[i]["Logo"],scale=.8,origin=(0,0,4.4),rotation_x=df_apollo.iloc[i]["Lat"],rotation_y=df_apollo.iloc[i]["Long"]*-1)
    LL= Entity(model="quad",enabled=False,texture=df_apollo.loc[i]["Logo"],scale=.8,origin=(0,0,4.4),rotation_x=df_apollo.iloc[i]["Lat"],rotation_y=df_apollo.iloc[i]["Long"]*-1)
    E = Sequence(1,Func(L.blink,duration=.5),loop=True)
    LE= Sequence(1,Func(LL.blink,duration=.5),loop=True)
    E.start() ; LE.start()
    dark_stations.append(L)
    light_stations.append(LL)
    i += 1
    
for ls in light_stations:
    ls.unlit=True

global intro

toggle_s = False
def toggle_stations():
    global toggle_s,track
    if not toggle_s:
        destroy(track)
        track = Audio(sound_file_name='.\Sound\Apollo.mp3', volume=30)
        if light_state:
            for ls in light_stations:
                ls.enabled=True
        else:
            for s in dark_stations:
                s.enabled=True
        toggle_s = True
    else:
        destroy(track)
        for s in dark_stations:
            s.enabled=False
        for ls in light_stations:
                ls.enabled=False
        toggle_s = False
        
        
A=Button(color=color.light_gray,scale=(.2,.2),origin=(2.6,1.8),texture=".\Texture\APOLLO B.jpg")
A.tooltip=Tooltip("This will show the places of landing sites of APOLLO missions")
A.on_click = toggle_stations
# ===========================================================================================================================



global track
back_sound = Audio(sound_file_name='.\Sound\Back_sound.mp3', loop=True,auto_destroy=False, autoplay=True, volume=1)




def opening():
    global track
    track = Audio(sound_file_name='.\Sound\Intro.mp3', volume=30)
        
invoke(opening,delay=4)






mute=False
def sound_on_or_off():
    global mute,track
    if not mute:
        destroy(track)
        back_sound.volume=0
        sound_button.texture=".\Texture\Soundoff.jpg"
        destroy(sound_button.tooltip)
        sound_button.tooltip=Tooltip("Enable the sound")
        mute=True
        
    else:
        mute=False
        back_sound.volume=30
        track.volume=30
        sound_button.texture=".\Texture\Soundon.jpg"
        destroy(sound_button.tooltip)
        sound_button.tooltip=Tooltip("Mute all Audios")
        

sound_button=Button(color=color.light_gray,scale=(.07,.07),origin=(-11.25,6),texture=".\Texture\Soundon.jpg")
sound_button.tooltip=Tooltip("Mute all Audios")
sound_button.on_click = sound_on_or_off


# global intro


#====== Class planet ===========================================================================================================
global name_text
name_text=Text("")
able_text=True
# for any sphere shapes
class Planet(Entity):
    global able_text , name_text
    def __init__(self,z,scale,texture,name,rotation_y,en):
        super().__init__()
        self.model = 'hh.obj'
        self.collider = 'sphere'
        self.z = z
        self.rotation_y=rotation_y
        self.scale = scale
        self.texture = texture
        self.name = name
        self.enabled=en
    # Displays Name of the planet on the screen
    def input(self, key):
        def text_abler():
            global able_text
            able_text = True
        global able_text , name_text
        if self.hovered and able_text:
            name_text=Text(self.name,position=mouse.position)
            name_text.appear(speed=0.15)
            able_text = False
            destroy(name_text, delay=len(self.name)*.3)# ممكن تتغير علي حسب سرعة اللي بيقرا الكلام
            invoke(text_abler, delay=2)
#=================================================================================================================




#====== our spheres ===========================================================================================================

sun = Planet(z=-1000,scale=200,texture=".\Texture\Sun.jpg",name="THE SUN",rotation_y=0,en=True)
earth = Planet(z=-150,texture=".\Texture\Earth.jpg",scale=25.7,name="THE EARTH",rotation_y=0,en=True)
Light_earth = Planet(z=-150,texture=".\Texture\Earth.jpg",scale=25.7,name="THE EARTH",rotation_y=0,en=True)
moon = Planet(z=0,texture=".\Texture\lroc_color_poles_4k.tif",name="",scale=7,rotation_y=-90,en=True)
light_moon = Planet(z=0,texture=".\Texture\lroc_color_poles_4k.tif",name="",scale=7,rotation_y=-90,en=True)
mentle = Planet(z=0,texture=".\Texture\mentle.jpg",name="Mentle layer",scale=5.439162,rotation_y=-90,en=False)
partial_melt = Planet(z=0,texture=".\Texture\partial.jpeg",scale=1.933924,name="Partial melt layer",rotation_y=0,en=False)
outer_core = Planet(z=0,texture=".\Texture\euvisdoCarringtonMap.jpg",name="Outer core layer",scale=1.329553,rotation_y=0,en=False)
core = Planet(z=0,texture=".\Texture\core.jpg",name="The core",scale=.966962127,rotation_y=0,en=False)
moon_layers=[mentle,partial_melt,outer_core,core]
entity_dict = {
                       light_moon:'Moon crust\n\n  O lighter minerals are crystallized and floated\n      to the surface to form the Moon crust.\n\n  O The lunar crust seems to be thinner on the\n      side of the Moon facing the Earth, and thicker\n      on the side facing away.\n\n  O The crust has some heights up to 11Km and\n      depressions up to 9Km',
                       moon: 'Moon crust\n\n  O lighter minerals are crystallized and floated\n      to the surface to form the Moon crust.\n\n  O The lunar crust seems to be thinner on the\n      side of the Moon facing the Earth, and thicker\n      on the side facing away.\n\n  O The crust has some heights up to 11Km and\n      depressions up to 9Km',
                       mentle: """Mentle layer\n\n  O The mantle is made denser minerals,\n      such as olivine and pyroxene.\n\n  O The thickness is about 1350 Km.\n\n  O Shallow Moonquakes originating on or near\n      the surface can be caused by meteoroid\n      impacts with the Moon.""",
                       partial_melt: """Partial Melt\n\n  O A partially molten layer with a thickness\n      of 93 miles (150 kilometers) surrounds\n      the iron core.\n\n  O This layer caused active volcanoes over\n      the moon long time ago.\n\n  O Deep moonquakes are caused by the\n      pull of Earth's gravity tugging and\n      stretching this layer""", 
                       outer_core: """Outer Core\n\n  O Surrounding the solid inner core is\n      a fluid outer core.\n\n  O The total diameter of the outer core\n      is about 410 miles (660 kilometers).\n\n  O It's hot enough to create a surrounding\n      molten liquid iron outer core\n      ,but not hot enough to warm the surface.""",
                       core: """Inner Core\n\n  O At the center is the Moon's dense,\n      metallic core.\n\n  O The core is largely composed of\n      iron and some nickel.\n\n  O The inner core is a solid mass about\n      300 miles (480 kilometers) in diameter.\n\n  O Temperature ranges between 1327°C\n      and 1427°C."""}

entity_name_text = Text(text='', color=color.white,scale=1.2,enabled=False)
# Makes sun exempt from the shader
sun.unlit = True
Light_earth.unlit=True
light_moon.unlit=True
mentle.unlit=True
partial_melt.unlit=True
outer_core.unlit=True
core.unlit=True
# light from sun
light = PointLight(position=(0,0,-1000),shadows=False)

moon_time = earth_time = sun_time = light_time = -np. pi



def mohsen():
    global paused,track
    if paused:
        destroy(track)
        track = Audio(sound_file_name='.\Sound\Day night.mp3', volume=30)
        paused=False
        global dispaly
        dispaly=[sun,earth,moon,light_moon,Light_earth]
    else:
        destroy(track)
        paused=True


D=Button(color=color.light_gray,scale=(.2,.2),origin=(-3.6,1.3),texture=".\Texture\D&N B.jpg")
D.tooltip=Tooltip("Display the Day and night cycle and our rotation in universie")
D.on_click=mohsen

light_moon.enabled=Light_earth.enabled=False

light_state=False
def light_on_or_off():
    global light_state
    if not light_state:
        moon.enabled=earth.enabled=False
        light_moon.enabled=Light_earth.enabled=True
        light_button.texture=".\Texture\on.png"
        destroy(light_button.tooltip)
        light_button.tooltip=Tooltip("Turn off lighting system and depend on sun light")
        light_state=True
        
    else:
        light_state=False
        moon.enabled=earth.enabled=True
        light_moon.enabled=Light_earth.enabled=False
        light_button.texture=".\Texture\off.png"
        destroy(light_button.tooltip)
        light_button.tooltip=Tooltip("Turn on lighting system beside sun light")
        

light_button=Button(color=color.light_gray,scale=(.07,.07),origin=(-9.4,6),texture=".\Texture\off.png")
light_button.tooltip=Tooltip("Turn on lighting system beside sun light")
light_button.on_click = light_on_or_off



def update():
    
    if mute:
        track.volume=0
    
    if not toggle:   
        camera.parent=screen
        screen.rotation_x-=(mouse.velocity[1]*mouse.left*100)
        screen.rotation_y+=(mouse.velocity[0]*mouse.left*100)
    else:
        camera.parent=outer_core
        

    if light_state and toggle_s:
        for ls in light_stations:
            ls.enabled=True
        for s in dark_stations:
            s.enabled=False
    elif (not light_state) and (toggle_s):
        for s in dark_stations:
            s.enabled=True
        for ls in light_stations:
            ls.enabled=False
    
    if True in flag:
        if light_state:
            n=0
            while n < len(flag):
                if flag[n]:
                    light_moonquakes[n].enabled=True
                    dark_moonquakes[n].enabled=False
                n+=1

        else:
            n=0
            while n < len(flag):
                if flag[n]:
                    dark_moonquakes[n].enabled=True
                    light_moonquakes[n].enabled=False
                n+=1

    global paused
    if not paused:
        # rotate on orbit
        global angle,earth_time,light_time
        angle = np.pi * 1 / 180
        
        earth_time+=1*time.dt
        radius_1 = 150
        earth.x =Light_earth.x= np.cos(earth_time+angle+20) *radius_1
        earth.z =Light_earth.z= np.sin(earth_time+angle+20) *radius_1
        
        light_time+=.09*time.dt
        radius_2 = 1000
        light.x = np.cos(light_time+angle) *radius_2
        light.z = np.sin(light_time+angle) *radius_2
        sun.x = np.cos(light_time+angle) *radius_2
        sun.z = np.sin(light_time+angle) *radius_2
        
        # rotate on axis
        for s in dispaly:
            if s == moon or s == light_moon:
                s.rotation_y-=time.dt*57
                for q in dark_moonquakes:
                    q.rotation_y-=time.dt*(57/2)
                for lq in light_moonquakes:
                    lq.rotation_y-=time.dt*(57/2)
                for a in dark_stations:
                    a.rotation_y-=time.dt*(57/2)
                for ls in light_stations:
                    ls.rotation_y-=time.dt*(57/2)
                    
                    
            if s ==earth or s==Light_earth:
                s.rotation_y+=time.dt*500
            if s == sun:
                s.rotation_y += time.dt*10
                
    if name_text:
        name_text.position=mouse.position
    global entity_name_text
    # Check if the mouse is hovering over an entity
    # Text("fuck you",position=(1,1))

    for entity in entity_dict.keys():
        if mouse.hovered_entity == entity and toggle:
            # Update the text and position of the Text entity
            entity_name_text.enabled=True
            entity_name_text.background=True
            entity_name_text.background_color=color.black33
            entity_name_text.text = entity_dict[entity]
            entity_name_text.position =(-.87,.4)
            break
    else:
        # If the mouse is not hovering over any entity, clear the text
        entity_name_text.enabled = False
    
    
    

toggle = False
# create a function that changes the position and scale of the layers
def toggle_layers():
    global toggle,track,dark_moonquakes,light_moonquakes,light_stations,dark_stations
    moonquakes_dropmenu.enabled=False
    Q.enabled=False
    A.enabled=False
    H.enabled=False
    global paused
    paused=True
    D.enabled=False      
    if not toggle:
# All the scales depend on real data !! the scale ia on the moon with ratio 1,737.4/7= 248.2
# All distances in Km are divided by factor 248.2
        destroy(track)
       
        moon.texture=light_moon.texture=".\Texture\lroc_color_poles_4k.tif"
        destroy(map_key)
        toggle_h=False
        
        track = Audio(sound_file_name='.\Sound\Layers.mp3', volume=30)
        for s in dark_moonquakes:
            s.enabled=False
        for s in light_moonquakes:
            s.enabled=False  
        toggle = True
        for l in moon_layers:
            l.enabled=True
        current_text.enabled=False
        mentle.animate_position((0,0,-1.8), duration=2)
        partial_melt.animate_position((0,0,-4), duration=2)
        outer_core.animate_position((0,0,-4.5), duration=2)
        core.animate_position((0,0,-5), duration=2)
        moon.name=light_moon.name="The Moon Crust"
        camera.parent=outer_core
        
        # camera.parent=screen   #in case you want to open camera rotation in "layers" mod

    else:
        destroy(track)
        toggle = False
        Q.enabled=True
        A.enabled=True
        H.enabled=True
        D.enabled=True
        moonquakes_dropmenu.enabled=True
        for l in moon_layers:
            l.enabled=False
        moon.name=light_moon.name=""
        current_text.enabled=True
        camera.set_position(value=(-10,0,0),relative_to=moon)
        mentle.animate_position((0,0,0), duration=2)
        partial_melt.animate_position((0,0,0), duration=2)
        outer_core.animate_position((0,0,0), duration=2)
        core.animate_position((0,0,0), duration=2)
        camera.position=(0,0,-20)
        camera.parent=screen
        

L=Button(text="",color=color.light_gray,scale=(.2,.2),origin=(3.7,1.8),texture=".\Texture\Layers B.jpg")
L.tooltip=Tooltip("This will show the Layers of The Moon depend on seismic data                  \n[Warning]\nSome features will be disabled while showing the layers")
L.on_click = toggle_layers

toggle_h=False

def topography():
    global toggle_h,track,map_key
    if not toggle_h:
        destroy(track)
        track = Audio(sound_file_name='.\Sound\Height map.mp3', volume=30)
        map_key=Panel(color=color.white,scale=((2*.1),(2*.21536)),texture=".\Texture\Mapkey.png",position=(.47,-.3),enabled=False)
        moon.texture=light_moon.texture=".\Texture\Topography.png"
        map_key.enabled=True
        toggle_h=True
    else:
        destroy(track)
        moon.texture=light_moon.texture=".\Texture\lroc_color_poles_4k.tif"
        toggle_h=False
        map_key.enabled=False

H=Button(text="",color=color.light_gray,scale=(.2,.2),origin=(2.6,.7),texture=".\Texture\Height B.jpg")
H.tooltip=Tooltip("This will show the Topographical height map of the Moon")
H.on_click = topography




current_text=Text()
moonquakes_by_year = {}
def show_moonquake(g):
    global current_text,dark_moonquakes,flag
    moonquake = df.loc[g]
    if flag[g]:
        if seen[g]:            
            dark_moonquakes[g].enabled=False
            light_moonquakes[g].enabled=False
            dark_moonquakes[g].texture='.\Texture\quakes.png'
            light_moonquakes[g].texture='.\Texture\quakes.png'
            seen[g]=flag[g]=False
            if not(True in flag):
                destroy(current_text)


        else:
            seen[g]=True
            destroy(current_text)
            light_moonquakes[g].texture='.\Texture\quakes selected.png'
            dark_moonquakes[g].texture='.\Texture\quakes selected.png'
            current_text= Text(text=f"  Moonquake {g+1}\n  Magnitude: {moonquake['Magnitude']}\n  Latitude: {moonquake['Lat']}\n  Longitude: {moonquake['Long']}\n  Date: {moonquake['Date']}\n  Time: {str(moonquake['H'])} : {str(moonquake['M'])} : {str(moonquake['S'])}", scale=1.5, position=(-0.87, .3), parent=camera.ui, background=True, color=color.white)
            screen.rotation_x=moonquake['Lat']
            screen.rotation_y=light_moonquakes[g].rotation_y
        

    else:
        destroy(current_text)
        current_text= Text(text=f"  Moonquake {g+1}\n  Magnitude: {moonquake['Magnitude']}\n  Latitude: {moonquake['Lat']}\n  Longitude: {moonquake['Long']}\n  Date: {moonquake['Date']}\n  Time: {str(moonquake['H'])} : {str(moonquake['M'])} : {str(moonquake['S'])}", scale=1.5, position=(-0.87, .3), parent=camera.ui, background=True, color=color.white)
        flag[g]=seen[g]=True
        if light_state:
            light_moonquakes[g].texture='.\Texture\quakes selected.png'
            dark_moonquakes[g].texture='.\Texture\quakes selected.png'
            light_moonquakes[g].enabled=True
            screen.rotation_x=moonquake['Lat']
            screen.rotation_y=light_moonquakes[g].rotation_y

            
        else:
            light_moonquakes[g].texture='.\Texture\quakes selected.png'
            dark_moonquakes[g].texture='.\Texture\quakes selected.png'
            dark_moonquakes[g].enabled=True
            screen.rotation_x=moonquake['Lat']
            screen.rotation_y=light_moonquakes[g].rotation_y

            
    
g=0
for g, row in df.iterrows():
    # get the year of the moonquake
    year = row["Year"]
    # if the year is not in the dictionary, create a new list for it
    if year not in moonquakes_by_year:
        moonquakes_by_year[year] = []
    # append the moonquake index to the list of that year
    moonquakes_by_year[year].append(g)
# create a list to store the dropdown menu buttons for each year
year_buttons = []
# loop through the dictionary of moonquakes by year
for year, indices in moonquakes_by_year.items():
    # create a list of buttons for the moonquakes in that year
    moonquake_buttons = [DropdownMenuButton(text=("Day "+str(df.loc[g]["Day"])+" ,at time "+str(df.loc[g]["H"])+":"+str(df.loc[g]["M"])+":"+str(df.loc[g]["S"])),position=(.3,.1),on_click=Func(show_moonquake, g)) for g in indices]
    for g in range(len(moonquake_buttons)):
        # set the origin of the button to the right
        moonquake_buttons[g].origin = (1.5, .5)
        # set the position of the button to the left of the year button
        moonquake_buttons[g].x = -1
    # create a dropdown menu button for the year with the list of moonquake buttons as its buttons argument
    year_button = DropdownMenu(f'Year {year}', buttons=moonquake_buttons)
    # append the year button to the list of year buttons
    year_buttons.append(year_button)
# create a dropdown menu for the moonquakes with the list of year buttons
moonquakes_dropmenu = DropdownMenu('Moonquakes', buttons=year_buttons)
# adjust the position and scale of the dropdown menu
moonquakes_dropmenu.position = (.6,.3)
moonquakes_dropmenu.color=color.white33
moonquakes_dropmenu.scale = (0.3, 0.066)


# The title on the app
Text.default_resolution = 2160 * Text.size

Text(text='your beautiful\n MOON',scale=4,origin=(-.02,-1.7),color=color.azure,font='Mokoto Demo.ttf')


Sky(texture=".\Texture\space.png")




# window.fps_counter.enabled= False
# window.cog_button.enabled= True
# window.entity_counter.enabled=False
# window.input_entity.enabled=False
window.borderless=True
window.fullscreen=True


EditorCamera(rotate_key="left mouse")
model.run()