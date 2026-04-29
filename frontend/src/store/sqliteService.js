import localforage from 'localforage';

localforage.config({ name: 'airport_sqlite_demo', storeName: 'atc_tables' });

export const SQLiteDB = {
    async query(table) {
        const data = await localforage.getItem(table);
        return data || [];
    },
    async insert(table, record) {
        const data = await this.query(table);
        const newData = [...data, { ...record, _id: Date.now() }];
        await localforage.setItem(table, newData);
        return newData;
    },
    async clear(table) {
        await localforage.setItem(table, []);
    }
};

// Initializing the 6 SQLite tables structurally
Promise.all([
    SQLiteDB.query('aircraft'),
    SQLiteDB.query('schedule'),
    SQLiteDB.query('prediction'),
    SQLiteDB.query('algorithm_switch_log'),
    SQLiteDB.query('flight_history'),
    SQLiteDB.query('emergency_events')
]).then(() => console.log("[SQLite Demo Database] Connected to Persistence Layer."));
