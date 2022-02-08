<!-- this is the big table contaning all the transactions in the block chain -->
<!-- ID | INPUT | SIZE | OUTPUT | EMOTE | DATE  -->

<!-- JS -->
<script>
    import BlockchainRow from './BlockchainRow.svelte'

    // Prop values set by the web pages
    export let table_data   // the blockchain data that gets displayed as a table
    export let milestones   // dictionary of currency thing milestones and their TX IDs

    let columns = Object.keys(table_data[0])    // dynamically getting the keys of the data and using that as column headers
    // const columns = ['ID', 'INPUT', 'SIZE', 'OUTPUT', 'EMOTE', 'DATE']

    let ascending = true                        // default sorting is by ascending ID (for now anyway)

    
    // Checks if the current TX is a milestone. If so, returns its milestone. Otherwise returns null.
    const checkMilestone = id => {
        if (id in milestones) {
            return milestones[id]
        } else {
            return null
        }
    }

    // Sorting the array of objects by a property
    const sortColumn = key => {           // -> https://stackoverflow.com/questions/7889006/sorting-arrays-in-javascript-by-object-key-value
        ascending = !ascending

        // checking if property is a string or a number (manual check for Emote field because they're all string except the first one, which is a 0)
        if (isNaN(table_data[0][key]) || key === 'EMOTE') {
            table_data = table_data.sort((a, b) => sortString(a[key], b[key]))
        } else {
            table_data = table_data.sort((a, b) => sortInt(a[key], b[key]))
        }
    }

    // Sorting array by integer value
    const sortInt = (a, b) => {
        if (ascending)  return a - b
        else            return a + b
    }
    // Sorting array by string value
    const sortString = (a, b) => {
        if (a < b)      return ascending ? -1 : 1   // if A comes before B: A is first if ascending
        if (a > b)      return ascending ? 1 : -1   // if A comes after B: A is first if descending

        return 0                                    // no change if they are the same
    }
</script>

<!-- HTML -->
<div class="table-container">
<table class="blockchain-table">
    <!-- The Table Column Headers -->
    <thead class="clickable">
        {#each columns as column}
            <th on:click={() => sortColumn(column)}>
                {column}
            </th>
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