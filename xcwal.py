from pathlib import Path
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "-font", help="Font name")

# Get inital color values

colorfile = Path.home() / ".cache" / "wal" / "colors"

def get_colors(path):
    if path.exists and not path.is_dir():
        with path.open() as f:
            return f.readlines()
    else:
        return "Error, could not read file"

unformat_c = get_colors(colorfile)

# from https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def hex_to_floats(h):
   return [int(h[i:i + 2], 16) / 255. for i in (0, 2, 4)]

def formatColors(col):
    cc = col[1:-1] # hex codes
    return hex_to_floats(cc) 

c = list(map(formatColors, unformat_c))

# Helpful guide for templating
# From https://github.com/dneustadt/hyper-wal/blob/master/index.js
c_index = {
        0: 'black',
        1: 'red',
        2: 'green',
        3: 'yellow',
        4: 'blue',
        5: 'magenta',
        6: 'cyan',
        7: 'white',
        8: 'lightBlack',
        9: 'lightRed',
        10: 'lightGreen',
        11: 'lightYellow',
        12: 'lightBlue',
        13: 'lightMagenta',
        14: 'lightCyan',
        15: 'lightWhite'
        }

# Font settings

font = "Menlo"
font_size = "12.0"
font_regular = f"{font}-Regular - {font_size}"
font_bold = f"{font}-Bold - {font_size}"

def formatOutput(line):
    if not "string" in line:
        return line
    else:
        if "font_regular" in line:
            return line.replace('font_regular', font_regular)
        if "font_bold" in line:
            return line.replace('font_bold', font_bold)

        index = line.find('>')+1
        if line[index + 1] == "<":
            key = line[index]
        else:
            key = line[index] + line[index+1]
        
        if key.isdigit():
            colorIndex = int(key)
        else:
            return line
        cc = c[colorIndex]
        col_str = f'{cc[0]} {cc[1]} {cc[2]} 1'
        return line.replace(key, col_str)

template_file = Path.home() / ".config" / "wal" / "templates" / "xcwal.dvtcolortheme"

if not (template_file.exists()):
    print("Creating template file at ~/.config/wal/templates")
    with open(os.getcwd() + "/xcwal.dvtcolortheme") as f:
        l = f.readlines()
        t = open(template_file, 'w')
        t.writelines(l)
        t.close()
        template_file = Path.home() / ".config" / "wal" / "templates" / "xcwal.dvtcolortheme"

template_lines = get_colors(template_file)
tt = list(map(formatOutput, template_lines))

output_path = Path.home() / "Library" / "Developer" / "Xcode" / "UserData" / "FontAndColorThemes"
if not (output_path.exists() and output_path.is_dir()):
    print("Making Xcode FontAndColorThemes directory")
    os.mkdir(str(output_path))

output = open(str(output_path / "xcwal.dvtcolortheme"), 'w')
output.writelines(tt)
output.close()

cached_theme_path = output_path / 'xcwal.xccolortheme'
if cached_theme_path.exists():
    os.remove(str(cached_theme_path))
    print("removing cached theme file")

print("Theme written — restart Xcode to see effect")
