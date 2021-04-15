import Link from 'next/link'

export default ({read}) => {
    return (
        <div>
            <h1>Reads Page</h1>
            {Object.keys(read).map((r,i) => (
            <div>
                <Link href="read/[id]" as={`/read/${r}`}>
                    <a>{read[r].title}</a>
                </Link> 
            </div>
            ))}
        </div>
        )
    }

export async function  getStaticProps(context) {
    const res = await fetch(`https://nilshah98.github.io/Knowledge-Lake/data/pocket.json`)
    const data = await res.json()

    return {
        props: {read: data}
    }

}