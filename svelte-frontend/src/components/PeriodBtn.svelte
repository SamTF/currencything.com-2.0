<!-- These are the buttons used to filter the Currency Thing Stats by a certain time period -->

<!-- JS -->
<script>
    // Imports
    import { createEventDispatcher } from 'svelte'

    // Props
    export let label = '1D'
    export let period = 1
    export let selected = false
    
    const dispatch = createEventDispatcher()
    function onClick () {
        console.log('emitting event...')
        dispatch('filter', {label, period})
    }
</script>

<!-- HTML -->
<button class="button" 
    class:selected={selected}
    on:click={onClick}>
    {label}
</button>