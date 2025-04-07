// Author        : CHAN Cheuk Hei
// Student Name  : CHAN Cheuk Hei
// Student ID    : 57270778
// Usage         : Main - React.js Component [InfoObjectDetection.jsx - Info.]

import Card from "./Card";
import CollapsibleSection from "./CollapsibleSection";

function InfoObjectDection() {
    return (
        <Card title="Information (How To Use) - Houseplant Type & Problems Detector">
            <h2> Upload your houseplant image for Plant Type Detection and Plant Problem Detection, <i>Be Sure to upload a image with clear view and good distance</i> </h2>
            <p> <i>The following items is the YOLO models classes for the detection query</i> </p>

            <CollapsibleSection title={<span><b><u>Plant Type Detection</u></b> - <i>plant_detect_9c_40e</i></span>}>
                <ul>
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

            <CollapsibleSection title={<span><b><u>Plant Problem Detection, Version 3</u></b> - <i>plant_diseases_v3_7c_70e_L</i></span>}>
                <ul>
                    <li>Leaf Brown Tip</li>
                    <li>Leaf Curling</li>
                    <li>Leaf Mildew</li>
                    <li>Leaf Rust</li>
                    <li>Leaf Spot</li>
                    <li>Leaf Wilting</li>
                    <li>Leaf Yellowing</li>
                </ul>
            </CollapsibleSection>

            <CollapsibleSection title={<span>Plant Problem Detection, Two Kind - <i>plant_disease_1c_60e</i></span>}>
                <ul>
                    <li><b>Unhealthy</b> Percentage</li>
                </ul>
            </CollapsibleSection>

            <CollapsibleSection title={<span>Plant Problem Detection, Version 1 - <i>plant_disease_4c_50e</i></span>}>
                <ul>
                    <li>Leaf Brown Tip</li>
                    <li>Leaf Mildew</li>
                    <li>Leaf Spot</li>
                    <li>Leaf Wilting</li>
                </ul>
            </CollapsibleSection>

            <CollapsibleSection title={<span>Plant Problem Detection, Version 2 / Large - <i>plant_diseases_v2_6c_50e</i> / <i>plant_diseases_v2_6c_55e_L</i></span>}>
                <ul>
                    <li>Leaf Brown Tip</li>
                    <li>Leaf Curling</li>
                    <li>Leaf Mildew</li>
                    <li>Leaf Spot</li>
                    <li>Leaf Wilting</li>
                    <li>Leaf Yellowing</li>
                </ul>
            </CollapsibleSection>
        </Card>
    );
}

export default InfoObjectDection;