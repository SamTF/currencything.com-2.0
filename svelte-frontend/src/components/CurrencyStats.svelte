<!-- This component holds all the Stat Cards -->
<!-- Updates their data when clicking on the Time Period buttons -->

<!-- JS -->
<script>
    // Imports
    import StatCard from '../components/StatCard.svelte'

    // Fetching Currency Thing Stats for the given time period
    async function fetchStats(period=0) {
        const URL = `http://localhost:3000/api/blockchain/stats?period=${period}`
        const res = await fetch(URL)
        const stats = await res.json()

        return stats
    }

    const promise = fetchStats(0)
</script>

<!-- HTML -->
<div class="currency-stats">

    <!-- Fetching the data, and displaying empty values while loading -->
    {#await promise}
        <StatCard label='currency things in the wild'           data='' />
        <StatCard label='currency things mined'                 data=''     colour='blue'   />
        <StatCard label='trades'                                data=''     colour='purple' />
        <StatCard label='user trades'                           data=''     colour='yellow' />
        <StatCard label='currently holding'                     data=''     colour='green' />
        <StatCard label='currency things was the biggest trade' data=''     colour='pink' />
    {:then stats}
        <StatCard label='currency things in the wild'           data={stats.supply} />
        <StatCard label='currency things mined'                 data={stats.supply}         colour='blue'   />
        <StatCard label='trades'                                data={stats.trades}         colour='purple' />
        <StatCard label='user trades'                           data={stats.user_trades}    colour='yellow' />
        <StatCard label='currently holding'                     data={stats.users}          colour='green' />
        <StatCard label='currency things was the biggest trade' data={stats.biggest_trade}  colour='pink' />
    {:catch error}
        <p style="color: red">{error.message}</p>
    {/await}
    
</div>