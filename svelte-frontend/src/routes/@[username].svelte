<!-- These are the user profiles! -->
<!-- Example URL: https://currencything.com/@Sam -->

<!-- Server Side Rendering! -->
<script context='module'>
    // This query is run before the page is rendered
    export async function load({url, params}) {
        const user = params.username

        // fetching the User's Blockchain data as JSON before rendering the page
        let res = await fetch('http://localhost:3000/api/blockchain/@' + user)
        let trades  = await res.json()

        // fetching the milestones
        let res2 = await fetch('http://localhost:3000/api/blockchain/milestones')
        let milestones = await res2.json()

        // fetching the user's stats
        let res3 = await fetch('http://localhost:3000/api/blockchain/stats/@' + user)
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

    import Blockchain from "../components/Blockchain.svelte"

    console.log(stats)
</script>



<!-- METADATA -->
<svelte:head>
    <title>{user}'s page</title>
    <meta name="description" content="this is the user profile of {user}">
</svelte:head>

<!-- HTML -->
<h1>{user}'s currency things</h1>

<section class="user-profile">
    <div class="user-profile-card shadow">
        <div class="avatar-container">
            <img src="https://currencything.com/static/images/avatars/216972321099874305.png" alt="{user}'s avatar" class="avatar shadow">
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

<Blockchain table_data={trades.reverse()} milestones={milestones}/>