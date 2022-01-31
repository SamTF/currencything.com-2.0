<!-- these are the statistics cards with cool info about the blockchain -->
<!-- they can be expanded/collapsed by clicking on them -->
<!-- expanding reveals a graph -->
<!-- expanding and collapsing produce sound fx -->

<!-- JS -->
<script>
    // Import transition animation
    import { slide } from 'svelte/transition'

    // Props
    export let data = 3             // the data to display in the text field
    export let label = 'title'      // text to display after the data
    export let colour = 'accent'    // background colour of the card


    // Use to show/hide the full graphs. Hidden by default.
    let toggled = false
    const toggle = () => {
        console.log('toggling graph...')
        toggled = !toggled
    }
</script>

<!-- HTML -->
<div class="stat-panel clickable" on:click={toggle}>
    <!-- Statistics Info Box -->
    <div class={`stat-card bg-${colour}`}>
        <h2>... <b>{data}</b> {label}</h2>
    </div>

    <!-- Expanded Graph -->
    <!-- This version keeps at panel on, but slides AND scales in the Graph -->
    <div class="graph-container">
        {#if toggled}
            <img src="https://currencything.com/static/graphs/supply.svg" alt="line_chart.svg" class="graph"  transition:slide='{{duration: 500}}'>
        {/if}
    </div>
</div>
