import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ChampInputFieldComponent } from '../champ-input-field/champ-input-field.component';
import { JsonFetcherService } from '../json-fetcher.service';

@Component({
  selector: 'app-champ-input-area',
  templateUrl: './champ-input-area.component.html',
  styleUrls: ['./champ-input-area.component.scss']
})
export class ChampInputAreaComponent implements AfterViewInit {

  counters: string[] = []
  Roles = Roles;
  useRoles: boolean = true;
  constructor(private fetcher: JsonFetcherService) { }
  @ViewChild('top') topChamp: ChampInputFieldComponent;
  @ViewChild('jg') jgChamp: ChampInputFieldComponent;
  @ViewChild('mid') midChamp: ChampInputFieldComponent;
  @ViewChild('bot') botChamp: ChampInputFieldComponent;
  @ViewChild('sup') suppChamp: ChampInputFieldComponent;

  inputFields : ChampInputFieldComponent[];

  ngAfterViewInit(): void {
  this.inputFields = [this.topChamp, this.jgChamp, this.midChamp, this.botChamp, this.suppChamp];
   const checkButton = document.querySelector('#getCountersButton');
   console.log(checkButton);
   checkButton!.addEventListener('click', this.checkCounters)
   const toggleLabelsButton = document.querySelector('#toggleRoleButton');
   toggleLabelsButton!.addEventListener('click', this.toggleLabels);
  }

  toggleLabels = () => {
    this.topChamp.toggleLabel()
    this.jgChamp.toggleLabel()
    this.midChamp.toggleLabel()
    this.botChamp.toggleLabel()
    this.suppChamp.toggleLabel()
    this.useRoles = !this.useRoles;
  }

  /**
   * better implementation of this
   * counter freq of all champs in counter list
   * then based on: tier, win rate into matchups, and occurences gen list
   */
  checkCounters = () => {
    // const data = this.fetcher.getChampData(this.topChamp.getValue())
    // const data2 = this.fetcher.getChampData(this.midChamp.getValue())
    // this.counters = []
    // const counters1: string[] = []
    // const counters2: string[] = []
    // if(data !== null && Object.keys(data.counters).includes('top')){
    //   //Object.keys(data.counters).forEach(element => { //get position
    //     Object.keys(data.counters['top']).forEach(i => {
    //       if(!counters1.includes(i)){
    //         counters1.push(i)
    //       }
    //     })
    //   //});
    // }
    // if(data2 !== null && Object.keys(data2.counters).includes('mid')){
    //   //Object.keys(data2.counters).forEach(element => { //get position
    //     Object.keys(data2.counters['mid']).forEach(i => {
    //       if(!counters2.includes(i)){
    //         counters2.push(i)
    //       }
    //     })
    //   //});
    // }
    // if(counters1.length > 0 && counters2.length > 0){
    //   let a = new Set(counters1);
    //   let b = new Set(counters2);
    //   let intersection = new Set(
    // [...a].filter(x => b.has(x)));
    //     this.counters = Array.from(intersection)
    // }

    if(this.useRoles){
      this.counters = this.extractMostFrequent(this.getCountersWithRoles());
      //Object.keys(this.getCountersWithRoles());
      //this.extractMostFrequent(this.getCountersWithRoles());
    } else {
      this.counters = this.extractMostFrequent(this.getCountersWithoutRoles());
      //Object.keys(this.getCountersWithoutRoles());
      
    }


  }

  getCountersWithRoles(){
    return this.getCounterFreq()
  }


  getCountersWithoutRoles(){
    return this.getCounterFreq()
  }

  getCounterFreq(){
    const counterFreq: Map<String, number> = new Map<String, number>();
    this.inputFields.forEach((field: ChampInputFieldComponent) => 
    {
      const roleCounters = (this.useRoles) ? this.fetcher.getCountersForRole(field.getValue(), field.getRole()):this.fetcher.getCounters(field.getValue())
      if(roleCounters != null){
         Object.keys(roleCounters).forEach((el: string) => {
          if(counterFreq.has(el)){
            counterFreq.set(el, counterFreq.get(el)! + 1)
          } else {
            counterFreq.set(el, 1)
          }
        });
      }
    })
    

    return counterFreq;
  }

  getChampImageUrl(champName: string, width = 40){
    return this.fetcher.getImageSource(champName, width);
  }

  extractMostFrequent(counterFreq: Map<String, number>){
    console.log('counter freq what about occ????: ', counterFreq);
    let totalOccs = 0;
    const freq = new Map<number, number>();
    counterFreq.forEach((val, key) => {
      console.log('key:', key, 'val',  val);
      totalOccs += val;;
      if(freq.has(val)){
        freq.set(val, freq.get(val)! + 1)
      } else {
        freq.set(val, 1)
      }
    });
    // const sorted = [...counterFreq].map(e =>{ return e[1];}).slice().sort(function(a, b) {
    //   return b-a; 
    // });
    const sortedFreq = new Map([...freq.entries()].sort(
      (a,b) => {
        console.log('a, b: ', a, b);
        return b[1] - a[1];
    }))

    const threshold = .4; 
    //want champ pool to typically contain 10-15 champs. Easier with a better filter function
    //for now it is naiive
    //a pool of size 10-15 in order will give best results, too many and its hard to read
    let maxItemChanges = 0;
    let freqSum = 0;
    sortedFreq.forEach((val, key) => {
      const freqVal = val/totalOccs;
      freqSum += freqVal
      console.log('freq val: ', freqVal);
      console.log('freqSum so far: ', freqSum);
      if(freqSum <= threshold){
        maxItemChanges += 1
      }
      sortedFreq.set(key, freqVal)
    })
    console.log('item changes: ', maxItemChanges);
    const sorted = new Map([...counterFreq.entries()].sort(
      (a,b) => {
        return b[1] - a[1];
    }))
    let prevVal: any = null;
    let itemChanges = 0;
    const best: string[] = []
    const filtered = new Map([...sorted.entries()].filter(
      (entry, index) => {
        const key = entry[0];
        const val = entry[1];
        if(prevVal !== null && prevVal !== val){
          itemChanges += 1
        }
        prevVal = val;
        if((itemChanges <= maxItemChanges && best.length < 20) || best.length < 10){
          best.push("" + key);
          //return true;
        }
        return true;
    }))
    console.log('filtered: ', filtered);
    //sorted largest to smallest
    console.log('best: ', best)
    return best;
  }

}



export enum Roles {
  Top='top',
  Jg='jg',
  Mid='mid',
  Bot='bot',
  Sup='sup'
}
