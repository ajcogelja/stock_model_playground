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
      this.counters = Object.keys(this.getCountersWithRoles());
      this.extractMostFrequent(this.getCountersWithRoles());
    } else {
      this.counters = Object.keys(this.getCountersWithoutRoles());
      this.extractMostFrequent(this.getCountersWithoutRoles());
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
    if(this.useRoles){
      this.inputFields.forEach((field: ChampInputFieldComponent) => 
      {
        const roleCounters = this.fetcher.getCountersForRole(field.getValue(), field.getRole())
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
    } else {
      this.inputFields.forEach((field: ChampInputFieldComponent) => 
      {
        const roleCounters = this.fetcher.getCounters(field.getValue())
        if(roleCounters != null){
          Object.keys(roleCounters).forEach((el: string) => {
            Object.keys(roleCounters[el]).forEach((elem: string) => {
              if(counterFreq.has(el)){
              counterFreq.set(elem, counterFreq.get(elem)! + 1)
            } else {
              counterFreq.set(elem, 1)
            }
            })
          });
        }
      })
    }

    return counterFreq;
  }

  extractMostFrequent(counterFreq: Map<String, number>){
    let totalOccs = 0;
    Object.values(counterFreq).forEach((occ) => {
      totalOccs += (+occ);
    });
    const sorted = [...counterFreq].map(e =>{ return e[1];}).slice().sort(function(a, b) {
      return b-a; 
    });
    const list: string[] = []
    var unique = [...new Set(sorted.values())]
    const sortedLen = sorted.length;
    let prevVal = unique[0];
    let run = true;
    sorted.forEach((key, val) => {
      if(val !== prevVal && list.length > sortedLen*2){
        run = false;
      }
      if(run){
        //list.push(key);
      }
    });
    console.log('counter freq: ', sorted);

    return list;
  }

}

export enum Roles {
  Top='top',
  Jg='jg',
  Mid='mid',
  Bot='bot',
  Sup='sup'
}
