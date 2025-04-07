// Author        : CHAN Cheuk Hei
// Student Name  : CHAN Cheuk Hei
// Student ID    : 57270778
// Usage         : Main - React.js Component [InfoRAG.jsx - Info.]

import Card from "./Card";
import CollapsibleSection from "./CollapsibleSection";

function InfoRAG(){
    return(
        <Card title="Information (How To Use) - Houseplant AI Agent">
            <h2> Enter your query at the "Houseplant AI Agent" - textarea section</h2>
            <ul>
                You should enter simple sentence for the query, below is example:
                <li>"Can you tell me about Chinese Evergreen?"</li>
                <li>"How to deal with the spots on Fiddle Leaf Fig?"</li>
                <li>"Can you tell me about watering?"</li>
                <li>"Can you list me 5 common pests?"</li>
            </ul>

            <p> <i>The following items is the Documents Dataset for the Retrieval-Augmented Generation (RAG)</i> </p>
            <CollapsibleSection title={<span><b><u>Plant Type Info</u></b> </span>}>
                <ul>
                    <li> <b>Chineses Evergreen</b> | 萬年青 | <i>Aglaonema</i> </li>
                    <li> <b>Aglaonema Red / Red Star</b> | 紅顏皇后 | <i>Aglaonema Red Variation</i> </li>
                    <li> <b>Asparagus Fern</b> | 文竹 | <i>Asparagus Setaceus</i> </li>
                    <li> <b>Fiddle Leaf Fig</b> | 芭比榕 | <i>Ficus Lyrata</i> </li>
                    <li> <b>Malabar Chestnut / Money Tree</b> | 發財樹 | <i>Pachira Aquatica</i> </li>
                    <li> <b>Emerald Ripple Pepper</b> | 皺葉椒草 | <i>Peperomia Caperata</i> </li>
                    <li> <b>Luna Red</b> | 紅寶石椒草 | <i>Peperomia Caperata Red Variation</i> </li>
                    <li> <b>Moon Valley Plant / Friendship Plant</b> | 皺葉冷水花 | <i>Pilea Mollis / Pilea Involucrata</i> </li>
                    <li> <b>Kusamaki / Buddhist Pine</b> | 羅漢松 | <i>Podocarpus Macrophyllus</i> </li>
                    <li> <b>Ogon Nishiki</b> | 黄金錦絡石 / 黄金錦 | <i>Trachelospermum Asiaticum Japan Variation</i> </li>
                </ul>
            </CollapsibleSection>

            <CollapsibleSection title={<span> <b><u>Basic Care</u></b> </span>}>
                <ul>
                    <li>
                        <strong>Plant Acquisition</strong>
                        <ul>
                            <li>Buy Plants / Purchase</li>
                            <li>Plant Location</li>
                            <li>Propagation</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Maintenance</strong>
                        <ul>
                            <li>Cleaning</li>
                            <li>Disposal</li>
                            <li>Feeding</li>
                            <li>Grooming</li>
                            <li>Potting / Potting Up / Repotting</li>
                            <li>Pruning</li>
                            <li>Water / Watering / Double Watering</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Environment</strong>
                        <ul>
                            <li>Drainage</li>
                            <li>Humidity</li>
                            <li>Lighting</li>
                            <li>Temperature</li>
                            <li>Wind</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Pest/Disease Control</strong>
                        <ul>
                            <li>Fungicides</li>
                            <li>Pesticides</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Tools/Materials</strong>
                        <ul>
                            <li>Container</li>
                            <li>Fertilizer</li>
                            <li>Potting Mix</li>
                            <li>Soil</li>
                            <li>Tools and Equipments</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Resources</strong>
                        <ul>
                            <li>Useful Website</li>
                        </ul>
                    </li>
                </ul>
            </CollapsibleSection>

            <CollapsibleSection title={<span> <b><u>Problems, Pests, Diseases</u></b> </span>}>

                <CollapsibleSection title={<span> <b><u>--Problems</u></b> </span>}>
                <ul>
                    <li>
                        <strong>Leaf Issues</strong>
                        <ul>
                            <li>Bleached Leaves</li>
                            <li>Brown Leaf Tips / Tips</li>
                            <li>Brown Leaves</li>
                            <li>Curling Leaves</li>
                            <li>Leaf eaten</li>
                            <li>Leaf Mottling</li>
                            <li>Leaf Scorch</li>
                            <li>Leaf Shed</li>
                            <li>Leaf Shoot Blackening</li>
                            <li>Leaf Spots</li>
                            <li>Leaves Changing Color</li>
                            <li>Leaves Turning Brown</li>
                            <li>Shrunken Wrinkled Leaves</li>
                            <li>Sudden Leaf Drop / Leaf Drop</li>
                            <li>Whitish Spots on Leaves</li>
                            <li>Wilting Leaves Stems</li>
                            <li>Yellow Leaf Edges</li>
                            <li>Yellow Leaves</li>
                            <li>Yellowing Patches on Leaves</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Growth Issues</strong>
                        <ul>
                            <li>Failure to Thrive / Failure to Flower / No Flowers / Spindly Growth</li>
                            <li>Flower Bud Drop</li>
                            <li>Leggy Growth</li>
                            <li>Loss of Vigor</li>
                            <li>Needle Drop</li>
                            <li>Plant Collapse</li>
                            <li>Plant Sprawl</li>
                            <li>Post Repotting Collapse</li>
                            <li>Premature Dormancy</li>
                            <li>Stunted Growth</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Environmental Stress</strong>
                        <ul>
                            <li>Oedema</li>
                            <li>Salt Burn</li>
                            <li>Sunburn</li>
                            <li>Wilting</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Pest/Disease Signs</strong>
                        <ul>
                            <li>Fine Stippling</li>
                            <li>Flying Insects</li>
                            <li>Fluffy White Wax</li>
                            <li>Fuzzy Gray Growth</li>
                            <li>Insects in Potting Media</li>
                        </ul>
                    </li>

                    <li>
                        <strong>Reddit Forum</strong>
                        <ul>
                            <li>Temperature Wrong</li>
                            <li>Too Little Fertilizer</li>
                            <li>Too Little Humidity</li>
                            <li>Too Little Light</li>
                            <li>Too Little Water</li>
                            <li>Too Much Fertilizer</li>
                            <li>Too Much Humidity</li>
                            <li>Too Much Light</li>
                            <li>Too Much Water</li>
                        </ul>
                    </li>
                </ul>
                </CollapsibleSection>

                <CollapsibleSection title={<span> <b><u>--Pests</u></b> </span>}>
                <ul>
                    <li>Ants</li>
                    <li>Aphids</li>
                    <li>Cyclamen Mites</li>
                    <li>Earwigs</li>
                    <li>Fungus Gnats</li>
                    <li>Leaf Miners</li>
                    <li>Leafhoppers</li>
                    <li>Mealybugs</li>
                    <li>(Red) Spider Mites</li>
                    <li>Scale Insects</li>
                    <li>Slugs and Snails</li>
                    <li>Thrips</li>
                    <li>Weevils</li>
                    <li>Whiteflies</li>
                </ul>
                </CollapsibleSection>

                <CollapsibleSection title={<span> <b><u>--Diseases</u></b> </span>}>
                <ul>
                    <li>Anthurium Blight</li>
                    <li>Bacterial Leaf Spots / Fungi Leaf Spots / Leaf Spot</li>
                    <li>Crown Rot / Crown Stem</li>
                    <li>Cymbidium Mosaic Virus / Mosaic Virus / Viruses</li>
                    <li>Gray Mold (Botrytis)</li>
                    <li>Leaf Gall</li>
                    <li>Powdery Mildew / White Powdery Coating</li>
                    <li>Roots Rot / Stems Rot</li>
                    <li>Rust Fungus</li>
                    <li>Soft Rot</li>
                    <li>Sooty Mold</li>
                </ul>
                </CollapsibleSection>

            </CollapsibleSection>

        </Card>
    )
}

export default InfoRAG