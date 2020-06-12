![Image](https://raw.githubusercontent.com/MrDoomy/PicturesRenamer/master/dev/images/pictures_renamer.png)

This is a simple script to massively rename pictures in a directory with the creation date.

This includes features like :
- Rename single file
- Rename all files in the same directory
- Specify a prefix for files
- Specify the format of the date
- Return the renaming operation logs

# Prerequisites

You need to have a Python environment on your computer and this package :

- PIL

```shell
   sudo pip install Pillow
```

# Usage

You can change the date format with `--template=[value]`. By default the date is returned like this : `%Y%m%d_%H%M%S`, but you can only display the time like this : `--template='%H%M%S'`. As you wish !

Here is the list of parameters of the template : 
- **%Y** : year
- **%m** : month
- **%d** : day
- **%H** : hour
- **%M** : minute
- **%S** : second

# Screenshot

![Image](https://raw.githubusercontent.com/MrDoomy/PicturesRenamer/master/dev/screenshots/computer.png)

# License

    Copyright (C) 2016 Damien Chazoule

    This program is free software : you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY ; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
