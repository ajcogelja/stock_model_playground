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
  Roles = Roles
  constructor(private fetcher: JsonFetcherService) { }
  @ViewChild('top') topChamp: ChampInputFieldComponent;
  @ViewChild('mid') midChamp: ChampInputFieldComponent;

  pressListener = (event: any) =>{
    console.log('top champ: ', this.topChamp)
    console.log('value: ', this.topChamp.getValue())
    //this.fetcher.getChampData(this.topChamp.getValue());
  }

  ngAfterViewInit(): void {
  //  const list = document.querySelector('app-champ-input-field')
  // list!.addEventListener('keypress', this.pressListener)
   const checkButton = document.querySelector('button');
   console.log(checkButton);
   checkButton!.addEventListener('click', this.checkCounters)
  }

  /**
   * better implementation of this
   * counter freq of all champs in counter list
   * then based on: tier, win rate into matchups, and occurences gen list
   */
  checkCounters = () => {
    const data = this.fetcher.getChampData(this.topChamp.getValue())
    const data2 = this.fetcher.getChampData(this.midChamp.getValue())
    this.counters = []
    const counters1: string[] = []
    const counters2: string[] = []
    if(data !== null && Object.keys(data.counters).includes('top')){
      //Object.keys(data.counters).forEach(element => { //get position
        Object.keys(data.counters['top']).forEach(i => {
          if(!counters1.includes(i)){
            counters1.push(i)
          }
        })
      //});
    }
    if(data2 !== null && Object.keys(data2.counters).includes('mid')){
      //Object.keys(data2.counters).forEach(element => { //get position
        Object.keys(data2.counters['mid']).forEach(i => {
          if(!counters2.includes(i)){
            counters2.push(i)
          }
        })
      //});
    }
    if(counters1.length > 0 && counters2.length > 0){
      let a = new Set(counters1);
      let b = new Set(counters2);
      let intersection = new Set(
    [...a].filter(x => b.has(x)));
        this.counters = Array.from(intersection)
    }


  }

}

export enum Roles {
  Top='top',
  Jg='jg',
  Mid='mid',
  Bot='bot',
  Sup='sup'
}
