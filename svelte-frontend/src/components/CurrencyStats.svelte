<!-- This component holds all the Stat Cards -->
<!-- Updates their data when clicking on the Time Period buttons -->

<!-- JS -->
<script>
    // Imports
    import StatCard from '../components/StatCard.svelte'
    import PeriodBtn from '../components/PeriodBtn.svelte'

    // Props
    export let stats = {}

    // Fetching Currency Thing Stats for the given time period
    async function fetchStats(period=0) {
        // getting the website's current domain
        const DOMAIN = import.meta.env.VITE_DOMAIN
        const URL = `${DOMAIN}/api/blockchain/stats?period=${period}`

        const res = await fetch(URL)
        const stats = await res.json()

        return stats
    }

    // Fetching all time currency thing stats
    let promise = fetchStats(0)

    // Re-fetching the stats data and reloading the UI when clicking a filter button
    function onPeriodFilter(event) {
        console.log('receving event')
        const {label, period} = event.detail

        // Checking if the clicked button is already selected
        if (periodButtons[label].selected) {
            console.log("Button is already selected!")
            return
        }

        // unselecting all other buttons (only one button can be selected at a time)
        for (const key in periodButtons) {
            periodButtons[key].selected = false
        }
        // selecting the button that was just clicked
        periodButtons[label].selected = true

        // fetching the data for the wanted period and refreshing the UI
        promise = fetchStats(period)

        // saving the fetched data to the local stats variable
        promise.then(value => {
            console.log(value)
            stats = value
            updatePhrase()  // update the time period phrase simultaneously
        })
    }

    // Dictionary of all the buttons and their values
    const periodButtons = {
        '1D':   {period: 1,     selected: false,    phrase: 'in the last 24h' },
        '7D':   {period: 7,     selected: false,    phrase: 'this week' },
        '31D':  {period: 31,    selected: false,    phrase: 'this month' },
        'ALL':  {period: 0,     selected: true,     phrase: 'total' },
    }

    
    let phrase = 'time period'
    // Gets the phrase property of the currently selected Period filter
    const updatePhrase = () => {
        phrase = Object.values(periodButtons)
            .filter(x => x.selected)[0]
            .phrase
    }
    updatePhrase()
</script>

<!-- HTML -->
<!-- The time period filtering buttons -->
<div class="button-container">
    {#each Object.entries(periodButtons) as [label, value]}
        <PeriodBtn label={label}
            period={value.period}
            selected={value.selected}
            on:filter={onPeriodFilter} />
    {/each}
</div>

<!-- The actual stat cards -->
<div class="currency-stats">
    <StatCard label='currency things in the wild'           data={stats.supply}         colour='accent'             graph={'supply'}/>
    <StatCard label='currency things mined'                 data={stats.mined}          colour='blue'   {phrase}    graph={'mined'}/>
    <StatCard label='trades'                                data={stats.trades}         colour='purple' {phrase}    graph={'trades'}/>
    <StatCard label='user trades'                           data={stats.user_trades}    colour='yellow' {phrase}    graph={'user_trades'}/>
    <StatCard label='people holding'                        data={stats.users.length}   colour='green'              graph={'holders'}/>
    <StatCard label='currency things was the biggest trade' data={stats.biggest_trade}  colour='pink'   {phrase}    graph={'biggest_trade'}/>    
</div>