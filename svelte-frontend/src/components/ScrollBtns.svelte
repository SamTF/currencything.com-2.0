<!-- this is the up/down button that scrolls smoothly to the top and bottom of the web page -->

<script>
    import SFX from '../sfx'

    // Scrolling to the wanted element by id -> https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView
    const scroll = id => {
        console.log(SFX.scroll_down)
        const elem = document.getElementById(id)    // getting the wanted element by its id
        elem.scrollIntoView({behavior: 'smooth'})   // !NOTE: must specify 'smooth' scroll here instead of css, otherwise it also 'smooth scrolls' when 'loading' a new page
        
        // Playing sound effects!
        if (id == 'top') {
            SFX.scroll_up.play()
        } else {
            SFX.scroll_down.play()
        }
        
    }
</script>

<!-- HTML -->
<div class="scroll-buttons">
    <img id="scroll-up"
        class="pixel-art clickable"
        src="/images/scroll_up.png" alt="scroll up" height="64px"
        on:click={() => scroll('top')}
    >

    <img id="scroll-down"
        class="pixel-art clickable"
        src="/images/scroll_down.png" alt="scroll down" height="64px"
        on:click={() => scroll('bottom')}
    >
</div>