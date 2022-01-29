<!-- This is the base page layout that all pages inherit from -->

<!-- Importing base components -->
<script>
    import ScrollBtns from '../components/ScrollBtns.svelte'
    import Logo from '../components/Logo.svelte'
    import SFX from '../sfx' // sound effects! l wonder if this slows down the page much?

    // Playing alternating clicking noises
    const clicks = [SFX.click1, SFX.click2]
    let clickCount = 0
    function click() {
        let i = clickCount % 2
        clicks[i].play()
        clickCount++
    }
</script>

<!-- Main HTML layout -->
<main class="page-layout" on:click={click}>

    <!-- Empty margin space -->
    <section id="left-margin">
        <Logo />
    </section>

    <!-- This is where the page content actually goes -->
    <section id=page-content>
        <!-- Top anchor point for the scroll buttons -->
        <div id="top"></div>

        <!-- Slot includes the content from the page components that inherit from this -->
        <slot></slot>

        <!-- Bottom anchor point for the scroll buttons -->
        <div id="bottom"></div>
    </section>
    
    <!-- Margin space with anchor buttons -->
    <section id="right-margin">
        <ScrollBtns />
    </section>

</main>
