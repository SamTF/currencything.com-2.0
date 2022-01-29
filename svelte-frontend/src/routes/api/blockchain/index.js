// # Basically a proxy for the backend Flask API
export async function get({params}) {
    const URL = 'http://localhost:5000/blockchain'
    const res = await fetch(URL)
    const data = await res.json()

    // Turning the EMOTE field into an image link
    // const newData = data.map(row => {
    //     let newEmote = getEmoteImg(row.EMOTE)

    //     return ({
    //         ...row,
    //         EMOTE: newEmote
    //     })
    // })

    // function getEmoteImg(emote) {
    //     const emoteDir = '/images/emotes/'
    //     const emoteFormat = '.webp'

    //     if (emote.startsWith(':'))  return emote

    //     return emoteDir + emote + emoteFormat
    // }

    return {
        status: 200,
        body: data
    }
}