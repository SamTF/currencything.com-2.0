<!-- The Individual rows in the blockchain table -->
<!-- Used in order to format data API appropriately for the front-end, because l don't think it would be a good idea to hardcode the formatting on the back-end -->

<script>
    // This component takes in a Row object with these properties
    export let row = {ID: 0, INPUT: 'I', SIZE: 1, OUTPUT: 'O', EMOTE: 'pog.png', DATE: 'today'}

    // Gets the path to the wanted emote on the local static directory
    function getEmoteImg(emote) {
        const emoteDir = '/images/emotes/'
        const emoteFormat = '.webp'

        return emoteDir + emote + emoteFormat
    }

    // Checks if an emote field has a respective emote image file Regex from: https://stackoverflow.com/questions/23476532/check-if-string-contains-only-letters-in-javascript
    // "True" emotes only contain letters.
    function emoteHasImg(emote) {
        // return (!/[^a-zA-Z]/.test(emote))
        return (/^[a-zA-Z]+$/.test(emote))
    }

    // Format the full date string into a more readable string
    // Maybe use this npm package in the future? https://www.npmjs.com/package/dateformat
    function formatDate(date) {
        const d = new Date(date + ' UTC')
        const fd = d.getDate() + '/' + (d.getMonth()+1) + '/' + (d.getFullYear()-2000)

        return fd
    }
</script>

<!-- HTML -->
<tr>
    <!-- TX ID -->
    <td>{row.ID}</td>

    <!-- TX Sender -->
    <td>
        <a href={row.INPUT == 'Currency Thing' ? '/' : `/@${row.INPUT}`}>
            {row.INPUT}
        </a>
    </td>

    <!-- Amount of Currency Things sent -->
    <td>{row.SIZE}</td>

    <!-- TX Receiver -->
    <td><a href={`/@${row.OUTPUT}`}>
        {row.OUTPUT}
    </a></td>

    <!-- Emote image -->
    <td>
        {#if emoteHasImg(row.EMOTE)}
            <img src={getEmoteImg(row.EMOTE)} alt={row.EMOTE} height="32px" loading='lazy'>
        {:else}
            {row.EMOTE}
        {/if}
    </td>

    <!-- Date timestamp -->
    <td full-date={row.DATE.slice(0, -4)}>
        {formatDate(row.DATE)}
    </td>
</tr>


<style>
    td {
        position: relative;
    }

    /* idea from here: https://stackoverflow.com/questions/2011142/how-to-change-the-style-of-the-title-attribute-inside-an-anchor-tag */
    td[full-date]:hover:after {
        content: attr(full-date);
        position: absolute;
        top: -100%;
        left: -100%;
        background-color: #f15050c4;
        border-radius: 8px;
        padding: 0.5rem;
    }
</style>