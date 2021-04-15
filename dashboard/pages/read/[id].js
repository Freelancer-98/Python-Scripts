
export default ({read}) => {

    return (
        <div>
            <h1>{read.title}</h1>
            <h2>Annotations</h2>
            <ol>
                {read.annotations.map(i => <li>{i}</li>)}
            </ol>
            <h2>Tags</h2>
            <ul>
                {read.tags.map(t => <li>{t}</li>)}
            </ul>
        </div>
    )
}

export async function getStaticPaths() {
    const res = await fetch(`https://nilshah98.github.io/Knowledge-Lake/data/pocket.json`)
    const data = await res.json()
    const paths = Object.keys(data).map(r => ({
        params: {id: r}
    }))

    return { paths, fallback: false }
}

export async function getStaticProps({ params }) {
    const res = await fetch(`https://nilshah98.github.io/Knowledge-Lake/data/pocket.json`)
    const data = await res.json()

    return {
        props: {read : data[params.id]}
    }
}