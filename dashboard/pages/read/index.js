import { promises as fs } from 'fs'
import path from 'path'
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

    const dataDir = path.join(process.cwd(), '../data')
    const rawData = await fs.readFile(dataDir + '/pocket.json', 'utf-8')
    const data = JSON.parse(rawData)

    return {
        props: {read: data}
    }

}