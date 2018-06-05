import os
import random

try:
	from termcolor import colored
except ImportError:
	"Use termcolor for better graphics"
	def colored(*args, **kwargs):
		return args[0] 


banner_eng = """
   ▄████████    ▄████████     ███      ▄██████▄     ▄████████  ▄█  
  ███    ███   ███    ███ ▀█████████▄ ███    ███   ███    ███ ███  
  ███    █▀    ███    ███    ▀███▀▀██ ███    ███   ███    ███ ███▌ 
  ███          ███    ███     ███   ▀ ███    ███  ▄███▄▄▄▄██▀ ███▌ 
▀███████████ ▀███████████     ███     ███    ███ ▀▀███▀▀▀▀▀   ███▌ 
         ███   ███    ███     ███     ███    ███ ▀███████████ ███  
   ▄█    ███   ███    ███     ███     ███    ███   ███    ███ ███  
 ▄████████▀    ███    █▀     ▄████▀    ▀██████▀    ███    ███ █▀   
                                                   ███    ███ 
"""

banner_jap_ver = ("""
    `                                
       MMh.                             
       mMMo              `-:/oso-       
       mMM:   ::/+osydmNMMMMMMMNd       
       mMM.  `dMMMNdNMMy+/:--.`         
       mMMd/.       NMM`  `:ss:         
    yN:mMMMMMd:://+yMMMdmNMMMMN         
   .MM:mMM-sMMNNMMNMMMdso+/mMM:         
   yMM.mMM  .:.    NMM`   `MMy          
  oMMm mMM        -MMd `.-yMMhsyhmNNy`  
  +MN- mMN -oossyhNMMMMMMMMMMMNmdhhys.  
   ``  mMN -hmmdhhyso+//:-.`::`         
       mMN      yh:`-:/+oshNMMN         
       mMN      mMMMMMMNmdhmMMy         
       mMN      hMM/.`     dMM.         
       mMN      yMM`      `MMd          
       mMN      yMM:-:/+osdMMNo         
       MMN      mMMMMMMNmdhyys+         
       yMN      hMMo-.`                 
        ..       +o                     
                                        
""",
"""
            `::`                        
            dMMM-   -/+/.               
            sMMM+`+mMMMMMh.             
            +MMMhmMN/`-mMMN`            
            sMMMMMh`   +MMM/            
            dMMMMh     .MMMs            
            NMMMM.     `MMMs            
           `MMMMh      -MMMo            
           `MMMMs      +MMM/            
            dMMMs      mMMN`            
            -hmd/     +MMMs             
                     -NMMm`             
                    -NMMN-              
                   :NMMm-               
                 -hMMNo`                
              .omMMd+`                  
             oyys/.    
""")


banner_jap_hor = ""
for line1, line2 in zip(banner_jap_ver[0].splitlines()[1:],banner_jap_ver[1].splitlines()[1:]):
	banner_jap_hor += line1 + line2[8:] + os.linesep

banner_jap_hor += os.linesep.join(banner_jap_ver[0].splitlines()[-5:])


__all__ = ['banner_jap_hor', 'banner_jap_ver', 'banner_eng']


def colorize(banner, use_highlights=False):
	colors = [
        "grey",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white"
	]
	highlights = [
        "on_grey",
        "on_red",
        "on_green",
        "on_yellow",
        "on_blue",
        "on_magenta",
        "on_cyan",
        "on_white",
	]

	cbanner = ""
	for c in banner:
		if not c.isspace():	# its a space
			cbanner += colored(
					c,
					random.choice(colors),
					random.choice(highlights) if use_highlights else None
				)
		else :
			cbanner += c

	return cbanner

"""
import satoricore.graphics; print (satoricore.graphics.banner_jap_hor)
print(satoricore.graphics.colorize(satoricore.graphics.banner_jap_hor))
"""