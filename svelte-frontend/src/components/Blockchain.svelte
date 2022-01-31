<!-- this is the big table contaning all the transactions in the block chain -->
<!-- ID | INPUT | SIZE | OUTPUT | EMOTE | DATE  -->

<!-- JS -->
<script>
    import BlockchainRow from './BlockchainRow.svelte'

    // Prop values set by the web pages
    export let table_data   // the blockchain data that gets displayed as a table
    export let milestones   // dictionary of currency thing milestones and their TX IDs

    let columns = Object.keys(table_data[0]) // dynamically getting the keys of the data and using that as column headers
    // const columns = ['ID', 'INPUT', 'SIZE', 'OUTPUT', 'EMOTE', 'DATE']

    
    // Checks if the current TX is a milestone. If so, returns its milestone. Otherwise returns null.
    const checkMilestone = id => {
        if (id in milestones) {
            return milestones[id]
        } else {
            return null
        }
    }
</script>

<!-- HTML -->
<div class="table-container">
<table class="blockchain-table">
    <!-- The Table Column Headers -->
    <thead>
        {#each columns as column}
            <th>{column}</th>
        {/each}
    </thead>

    <!-- The Table Rows -->
    <tbody>
        <!-- Creating a BlockchainRow element for each row in the data array -->
        {#each table_data as row}
            <BlockchainRow {row} milestone={checkMilestone(row.ID)}/>
        {/each}
    </tbody>
</table>
</div>