<!-- these are the statistics cards with cool info about the blockchain -->
<!-- they can be expanded/collapsed by clicking on them -->
<!-- expanding reveals a graph -->
<!-- expanding and collapsing produce sound fx -->

<!-- JS -->
<script>
    import SFX from '../sfx'

    // Import transition animation
    import { slide } from 'svelte/transition'

    // Props
    export let data                 // the data to display in the text field
    export let label = 'title'      // text to display after the data
    export let colour = 'accent'    // background colour of the card
    export let phrase = ''          // phrase to display at the end, if any (ex: in the last 24h, this week, total)
    export let graph = ''           // the name of the graph SVG file to display
    export let svg_data


    // Use to show/hide the full graphs. Hidden by default.
    let toggled = false
    const toggle = () => {
        console.log('toggling graph...')
        toggled = !toggled

        // playing sfx for opening and closing
        if(toggled) SFX.open.play()
        else        SFX.close.play()
    }
</script>

<!-- HTML -->
<div class="stat-panel clickable" on:click={toggle}>
    <!-- Statistics Info Box -->
    <div class={`stat-card bg-${colour}`}>
        <!-- Only display data if there is data to display -->
        {#if data !== null}
            <h2>...<b>{data}</b> {label} {phrase}</h2>
        <!-- otherwise just display the label -->
        {:else}
            <h2>{label}</h2>
        {/if}
    </div>

    <!-- Expanded Graph -->
    <!-- This version keeps at panel on, but slides AND scales in the Graph -->
    <div class="graph-container">
        <!-- Loading image from disk -->
        {#if toggled && !svg_data}
            <img src={`/graphs/${graph}.svg`} alt={`/graphs/${graph}.svg`} class="graph"  transition:slide='{{duration: 600}}'>
        
        <!-- Rendering given inline SVG -->
        {:else if toggled && svg_data}
            <svg alt={`/graphs/${graph}.svg`} class="graph"  transition:slide='{{duration: 600}}'
                xmlns:xlink="http://www.w3.org/1999/xlink" width="576pt" height="432pt" viewBox="0 0 576 432" xmlns="http://www.w3.org/2000/svg" version="1.1">
                {@html svg_data}
            </svg>  
        {/if}
    </div>
</div>
