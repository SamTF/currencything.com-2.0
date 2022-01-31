<!-- This component holds all the Stat Cards -->
<!-- Updates their data when clicking on the Time Period buttons -->

<!-- JS -->
<script>
    // Imports
    import StatCard from '../components/StatCard.svelte'
</script>

<!-- HTML -->
<div class="currency-stats">
    <StatCard label='currency things in the wild' />
    <StatCard label='currency things mined'                 colour='blue'   />
    <StatCard label='trades'                                colour='purple' />
    <StatCard label='user trades'                           colour='yellow' />
    <StatCard label='people holding'                        colour='green' />
    <StatCard label='currency things was the biggest trade' colour='pink' />
</div>