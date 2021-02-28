import { Location } from "./location";

export class Threat {
    id:number; 
    monsterName:string; 
    dangerLevel:string; 
    location:Location = new Location();
}