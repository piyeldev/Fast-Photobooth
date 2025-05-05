# Fast Photo
A free and open-source photobooth software tool that helps small hobbyists!

#### It started out as a programming project by me, an SSLG officer in our school, deciding to make the photobooth process easier and less time consuming.



# Bugs and Feature Implementation List
#### Low priority bugs/planned implementation:
1. add "Empty" named frameview combo box when no frame presets are set
2. implement detach button above the camera view
3. implement responsivity in app
4. Implement the deletion of placeholders (Frame Editor)
5. If in a case where the number of images is more than the number of placeholders (becuse of deletion activities), prompt the user to delete 1 or more image.
6. Implement deletion of qrcode placeholder

#### Medium Priority Bugs/Planned Implementation:
1. Grey out the buttons when no preset has been made before (Frame Editor)
2. clear text in frame path button after pressing the delete button (frame editor) Bug appears when no frame is available anymore
3. Clear image in viewport after deleting a preset first, then replace it with the available one or the one active in the frame preset dropdown. If frame preset is empty, remove the image in the viewport. (Frame Editor)

# Development
1. Clone the repository
```
git clone https://github.com/piyeldev/Fast-Photo.git
```

2. Create virtual environment

```
cd Fast-Photo
python -m venv .venv
```
3. Install packages
```
pip install -r requirements.txt
```
4. Run program
```
python main.py
```
If you're in linux:
```
QT_QPA_PLATFORM=xcb python main.py
```
or put this in your ~/.bashrc or ~/.zshrc
```
export QT_QPA_PLATFORM=xcb
```
this will fix flickering of ui in wayland (linux)
