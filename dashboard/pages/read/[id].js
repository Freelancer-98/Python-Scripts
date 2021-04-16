import { promises as fs } from 'fs'
import path from 'path'

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
    const dataDir = path.join(process.cwd(), '../data')
    const rawData = await fs.readFile(dataDir + '/pocket.json', 'utf-8')
    const data = JSON.parse(rawData)
    
    const paths = Object.keys(data).map(r => ({
        params: {id: r}
    }))

    return { paths, fallback: false }
}

export async function getStaticProps({ params }) {
    const dataDir = path.join(process.cwd(), '../data')
    const rawData = await fs.readFile(dataDir + '/pocket.json', 'utf-8')
    const data = JSON.parse(rawData)

    return {
        props: {read : data[params.id]}
    }
}