// This script contains all the Sound FX used in the website

const sfxDir = '/static/sfx/'

let SFX = {
    scroll_down: 'filesspill1.mp3',
    scroll_up: 'filesspill2.mp3',
    honk: '',
    click1: '',
    click2: '',
}

// The Audio components must be created client-side
if(typeof Audio != "undefined") {
    // Browser-only code -> https://stackoverflow.com/questions/34757854/referenceerror-audio-is-not-defined
    SFX = {
        scroll_down:    new Audio(sfxDir + 'filesspill1.mp3'),
        scroll_up:      new Audio(sfxDir + 'filesspill2.mp3'),
        honk:           new Audio(sfxDir + 'honk.mp3'),
        click1:         new Audio(sfxDir + 'click1.ogg'),
        click2:         new Audio(sfxDir + 'click2.ogg'),
    }
}


export default SFX