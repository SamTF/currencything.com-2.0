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

        return {props: {user, trades, milestones}}
    }
</script>

<!-- Regular client side JS -->
<script>
    export let user         // the name of the user
    export let trades       // the blockchain filtered to show only their transactions
    export let milestones   // all currency thing milestones

    import Blockchain from "../components/Blockchain.svelte"
</script>



<!-- METADATA -->
<svelte:head>
    <title>{user}'s page</title>
    <meta name="description" content="this is the user profile of {user}">
</svelte:head>

<!-- HTML -->
<h1>{user}'s currency things</h1>
<p style="text-align: center;">Welcome to {user}'s currency thing page!</p>

<section class="user-profile">
    <div class="avatar-container">
        <img src="https://currencything.com/static/images/avatars/216972321099874305.png" alt="{user}'s avatar" class="avatar">
    </div>

    <div class="user-info">
        <div class="user-things">
            <p>{user} has XXXX currency things</p>
        </div>

        <div class="stats">
            <p>...has mined <b>XXX</b> things</p>
            <p>...has received <b>XXX</b> things</p>
            <p>...has sent <b>XXX</b> things</p>
            <p>...participated in <b>XXX</b> trades</p>
            <p>...biggest gift sent was <b>XXX</b> things</p>
            <p>...biggest gift received was <b>XXX</b> things</p>
        </div>
    </div>
</section>

<Blockchain table_data={trades.reverse()} milestones={milestones}/>