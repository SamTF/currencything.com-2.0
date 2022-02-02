<!-- This component holds all the Stat Cards -->
<!-- Updates their data when clicking on the Time Period buttons -->

<!-- JS -->
<script>
    // Imports
    import StatCard from '../components/StatCard.svelte'
    import PeriodBtn from '../components/PeriodBtn.svelte'

    // Fetching Currency Thing Stats for the given time period
    async function fetchStats(period=0) {
        const URL = `http://localhost:3000/api/blockchain/stats?period=${period}`
        const res = await fetch(URL)
        const stats = await res.json()

        return stats
    }

    let promise = fetchStats(0)

    function onPeriodFilter(event) {
        console.log('receving event')
        const period = event.detail
        console.log(period)
    }

    const periodButtons = {
        '1D': 1,
        '7D': 7,
        '31D': 31,
        'ALL': 0
    }
</script>

<!-- HTML -->
<div class="button-container">
    {#each Object.entries(periodButtons) as [label, period]}
        <PeriodBtn label={label}   periodValue={period}   on:filter={onPeriodFilter} selected={false}/>
    {/each}
    <!-- <PeriodBtn label='1D'   periodValue=1   on:filter={onPeriodFilter} selected={false}/>
    <PeriodBtn label='7D'   periodValue=7   on:filter={onPeriodFilter} selected={false}/>
    <PeriodBtn label='31D'  periodValue=31  on:filter={onPeriodFilter} selected={false}/>
    <PeriodBtn label='ALL'  periodValue=0   on:filter={onPeriodFilter} selected={false}/> -->
</div>

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