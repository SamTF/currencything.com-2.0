<!-- These are the user profiles! -->
<!-- Example URL: https://currencything.com/@Sam -->

<!-- Server Side Rendering! -->
<script context='module'>
    // This query is run before the page is rendered
    export async function load({url, params}) {
        // getting the username in the url: /@Username
        const user = params.username

        // getting the website's current domain
        const DOMAIN = import.meta.env.VITE_DOMAIN

        // fetching the User's Blockchain data as JSON before rendering the page
        let res = await fetch(`${DOMAIN}/api/blockchain/@${user}`)

        // error handling if the user doesn't exist
        if (!res.ok) {
            throw new Error(`User ${user} not found :(`)
        }
        let trades  = await res.json()

        // fetching the milestones
        let res2 = await fetch(`${DOMAIN}/api/blockchain/milestones`)
        let milestones = await res2.json()

        // fetching the user's stats
        let res3 = await fetch(`${DOMAIN}/api/blockchain/stats/@${user}`)
        let stats = await res3.json()

        return {props: {user, trades, milestones, stats}}
    }
</script>

<!-- Regular client side JS -->
<script>
    export let user         // the name of the user
    export let trades       // the blockchain filtered to show only their transactions
    export let milestones   // all currency thing milestones
    export let stats        // the user's fun fact statistics

    // IMPORTS
    import Blockchain from '../components/Blockchain.svelte'
    import StatCard from '../components/StatCard.svelte'
    import Meta from '../components/Meta.svelte'
    

    // Fetching graphs after loading the page because it takes ~200ms
    async function fetchGraphs() {
        let res = await fetch('http://localhost:3000/api/blockchain/graphs/@' + user)
        let graphs = await res.json()
        return graphs
    }

    let promise = fetchGraphs()
</script>



<!-- METADATA -->
<svelte:head>
    <title>{user}'s page</title>

    <!-- Meta -->
    <Meta title="{user}'s Currency Things" description="{user} has {user.balance} currency things! 💰" />
</svelte:head>

<!-- HTML -->
<h1>{user}'s currency things</h1>

<section class="user-profile">
    <div class="user-profile-card shadow">
        <div class="avatar-container">
            <img src="/images/avatars/{user}.webp" alt="{user}'s avatar" class="avatar shadow">
        </div>
    
        <div class="user-info">
            <div class="user-things">
                <h1>{user}</h1> <p>has {stats.balance} currency things</p>
            </div>
    
            <div class="stats">
                <p>...has mined <b>{stats.mined}</b> things</p>
                <p>...has received <b>{stats.things_received}</b> things</p>
                <p>...has sent <b>{stats.things_sent}</b> things</p>
                <p>...participated in <b>{stats.trades}</b> trades</p>
                <p>...biggest gift sent was <b>{stats.biggest_sent}</b> things</p>
                <p>...biggest gift received was <b>{stats.biggest_received}</b> things</p>
            </div>
        </div>
    </div>
    
</section>

<br>
<p style="text-align: center;">Welcome to {user}'s currency thing page!</p>

<!-- Stat Cards with Graphs -->
<div class="currency-stats">
    <!-- Using Await block to allow for fetching this data AFTER the page has been rendered -->
    {#await promise}
        <StatCard label='networth'  data={null} graph={`${user} networth`}  colour='blue' />
        <StatCard label='trades'    data={null} graph={`${user} trades`}    colour='purple' />
    {:then graphs} 
        <StatCard label='networth'  data={null} svg_data={graphs.networth}  colour='blue' />
        <StatCard label='trades'    data={null} svg_data={graphs.trades}    colour='purple' />
    {/await}
</div>

<Blockchain table_data={trades.reverse()} milestones={milestones}/>