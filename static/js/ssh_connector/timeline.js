class Timeline {
    /*
    * ts : timestamp
    * rec : record
    * rawRecords
    *   'timestamp[59294838085]recordcontentendtimestamp\ntimestamp[59294838085]recordcontentendtimestamp...'
    * ts_rec_array
    *   [ timestamp[59294838085]recordcontent, ... ]
    * ts_rec_array
    *   { ts:recordcontenct, ... }
    * */
    constructor(container)  {
        this.container = container;
    };
    
    open = (ws, rawRecords) => {
        // Get basic data
        this.ts_rec_array   = this.get_ts_rec_array(rawRecords);
        this.ts_rec_map     = this.get_ts_rec_map(this.ts_rec_array);
        this.startTs        = this.ts_rec_array[0].substring(11,22);
        this.stopTs         = this.ts_rec_array[this.ts_rec_array.length - 1].substring(11,22);
        
        this.timeoutArray = [];
        this.playing = NaN;
        this.next = NaN;
        
        ws.close()

    };
    
    get_ts_rec_array = (rawRecords) => {
        return rawRecords.data.split('endtimestamp\n');
    };
    get_ts_rec_map = (ts_rec_array) => {
        let _map = new Map();
        for (let ts_rec of ts_rec_array) {
            _map.set(parseInt(ts_rec.substring(11,22)), ts_rec.substring(22))
        }
        return _map
    };
     
    play = (startTimestamp = this.startTs) => {
        let container = this.container;
        let timeOutArray = this.timeoutArray;
        for (let [ts, rec] of this.ts_rec_map) {
            (function (ts, rec) {
                let diff = ts - startTimestamp;
                if (diff < 0) {return}
                let _t = setTimeout(function (){
                    container.write(rec)
                }, ts - startTimestamp); 
                timeOutArray.push(_t);
            })(ts, rec)
        }
    };
    
    start_play = () => {
        this.play(this.startTs);
    };
    
    pause = () => {
        for (let timeoutID of this.timeoutArray) {
            clearTimeout(timeoutID)
        }
    } 
}

export {Timeline}