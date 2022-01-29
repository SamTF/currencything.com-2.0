<!-- This is the Currency Thing clown logo in the top-left that is present in every page -->
<!-- it functions as a link back to the main page (except on the main page itself) -->
<!-- it is hidden on mobile -->

<script>
    import SFX from '../sfx'

    const honk = () => {
        SFX.honk.play()
    }
</script>

<!-- HTML -->
<a href="/">
    <img class="logo clickable" 
        src="/images/clown.webp" alt="clown logo"
        title="what is this, some kinda currency thing? 🤡"
        on:click={honk}>
</a>
